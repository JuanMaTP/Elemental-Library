from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from author.models import Author


class AuthorCreationTestCase(APITestCase):

    def setUp(self):
        self.staff = User.objects.create_user(username='librarian', password='pass', is_staff=True)
        self.client.force_authenticate(user=self.staff)

    def test_author_creation(self):
        data = {'name': 'Test Author', 'birth_date': '2020-09-01', 'gender': 'F'}

        response = self.client.post('/api/authors/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(pk=response.data['id'])
        response = self.client.get(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], author.name)

    def test_author_creation_failed(self):
        data = {'name': '', 'birth_date': '', 'gender': ''}

        response = self.client.post('/api/authors/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_user_cannot_create_author(self):
        self.client.force_authenticate(user=None)

        response = self.client.post('/api/authors/', {'name': 'A', 'birth_date': '2000-01-01', 'gender': 'F'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
