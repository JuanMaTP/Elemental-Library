from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book, BookUnit


class BookCreationTestCase(APITestCase):

    def setUp(self):
        self.staff = User.objects.create_user(username='librarian', password='pass', is_staff=True)
        self.client.force_authenticate(user=self.staff)

    def test_book_creation(self):
        data = {'name': 'Test Book', 'description': 'A Test Book description', 'author': []}

        response = self.client.post('/api/books/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_creation_failed(self):
        response = self.client.post('/api/books/', {'author': []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_staff_can_create_books(self):
        member = User.objects.create_user(username='member', password='pass')
        self.client.force_authenticate(user=member)

        response = self.client.post('/api/books/', {'name': 'Book', 'description': 'Text'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_users_can_read_but_not_write(self):
        self.client.force_authenticate(user=None)

        self.assertEqual(self.client.get('/api/books/').status_code, status.HTTP_200_OK)
        response = self.client.post('/api/books/', {'name': 'Book', 'description': 'Text'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookUnitCreationTestCase(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(name='Book for BookUnit', description='A Book for a BookUnit')
        self.staff = User.objects.create_user(username='librarian', password='pass', is_staff=True)
        self.client.force_authenticate(user=self.staff)

    def test_book_unit_creation(self):
        response = self.client.post(f'/api/books/{self.book.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_unit = BookUnit.objects.get(book=self.book)
        self.assertEqual(len(book_unit.serial), 16)
        self.assertEqual(len(response.data['book_units']), 1)

        response = self.client.get(f'/api/books/{self.book.id}/{book_unit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_unit_creation_with_serial(self):
        response = self.client.post(f'/api/books/{self.book.id}/', {'serial': 'ABCDEFGHIJKLMNOP'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BookUnit.objects.filter(book=self.book, serial='ABCDEFGHIJKLMNOP').exists())

    def test_book_update(self):
        response = self.client.put(f'/api/books/{self.book.id}/', {'name': 'Updated Book name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Book name')
