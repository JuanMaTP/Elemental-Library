from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

REGISTRATION = {'username': 'test_user', 'password': '123', 'birth_date': '2020-09-01', 'gender': 'O', 'type': 'VI'}


class RegistrationTestCase(APITestCase):

    def test_person_creation(self):
        response = self.client.post('/api/people/', REGISTRATION)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=response.data['id'])
        self.assertEqual(user.person.type, 'VI')
        self.assertTrue(user.check_password('123'))

        response = self.client.get(f'/api/people/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)

    def test_person_creation_failed(self):
        data = {'username': '', 'password': '', 'birth_date': '', 'gender': '', 'type': ''}

        response = self.client.post('/api/people/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileUpdateTestCase(APITestCase):

    def setUp(self):
        user_id = self.client.post('/api/people/', REGISTRATION).data['id']
        self.user = User.objects.get(pk=user_id)

    def test_user_can_update_own_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(f'/api/people/{self.user.id}/', {'username': 'renamed'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'renamed')

    def test_user_cannot_update_someone_else(self):
        other = User.objects.create_user(username='other', password='pass')
        self.client.force_authenticate(user=other)

        response = self.client.patch(f'/api/people/{self.user.id}/', {'username': 'hijacked'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
