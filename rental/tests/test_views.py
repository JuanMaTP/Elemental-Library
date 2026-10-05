from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book, BookUnit
from rental.models import Rental
from rental.tasks import check_rentals_return


def register(client, username):
    data = {'username': username, 'password': '123', 'birth_date': '2000-01-01', 'gender': 'O', 'type': 'ST'}
    return User.objects.get(pk=client.post('/api/people/', data).data['id'])


class RentalTestCase(APITestCase):

    def setUp(self):
        # A staff user without a Person row, so user and person ids differ
        User.objects.create_user(username='librarian', password='pass', is_staff=True)

        self.book = Book.objects.create(name='A test Book', description='A Book')
        self.book_unit = BookUnit.objects.create(book=self.book, serial='TestSerialNumber')
        self.user = register(self.client, 'reader')
        self.client.force_authenticate(user=self.user)

    def borrow(self):
        return self.client.post('/api/rentals/borrow/', {'book_unit': self.book_unit.id})

    def test_rental_creation(self):
        response = self.borrow()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rental = Rental.objects.get(pk=response.data['id'])
        self.assertEqual(rental.person, self.user.person)
        self.assertEqual(rental.person_type, 'ST')
        self.book_unit.refresh_from_db()
        self.assertTrue(self.book_unit.borrowed)

    def test_cannot_borrow_a_borrowed_unit(self):
        self.borrow()

        response = self.borrow()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rental_creation_failed(self):
        response = self.client.post('/api/rentals/borrow/', {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_user_cannot_borrow(self):
        self.client.force_authenticate(user=None)

        self.assertEqual(self.borrow().status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_book_unit(self):
        rental_id = self.borrow().data['id']

        response = self.client.put(f'/api/rentals/return/{rental_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['return_date'])
        self.book_unit.refresh_from_db()
        self.assertFalse(self.book_unit.borrowed)

    def test_only_the_renter_can_return(self):
        rental_id = self.borrow().data['id']
        self.client.force_authenticate(user=register(self.client, 'someone_else'))

        response = self.client.put(f'/api/rentals/return/{rental_id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_saving_an_open_rental_keeps_the_unit_borrowed(self):
        rental = Rental.objects.get(pk=self.borrow().data['id'])

        rental.save()

        self.book_unit.refresh_from_db()
        self.assertTrue(self.book_unit.borrowed)


class OverdueRentalsTaskTestCase(APITestCase):

    def setUp(self):
        book = Book.objects.create(name='A test Book', description='A Book')
        self.overdue_unit = BookUnit.objects.create(book=book, serial='OverdueSerial000')
        self.recent_unit = BookUnit.objects.create(book=book, serial='RecentSerial0000')
        person = register(self.client, 'reader').person

        self.overdue = Rental.objects.create(book_unit=self.overdue_unit, person=person)
        Rental.objects.filter(pk=self.overdue.pk).update(
            rental_date=timezone.now() - settings.RENTAL_PERIOD - timedelta(hours=1))
        self.recent = Rental.objects.create(book_unit=self.recent_unit, person=person)

    def test_returns_only_overdue_rentals(self):
        returned = check_rentals_return()

        self.assertEqual(returned, 1)
        self.overdue.refresh_from_db()
        self.recent.refresh_from_db()
        self.assertIsNotNone(self.overdue.return_date)
        self.assertIsNone(self.recent.return_date)
        self.overdue_unit.refresh_from_db()
        self.assertFalse(self.overdue_unit.borrowed)
