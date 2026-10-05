from rest_framework import status
from rest_framework.test import APITestCase


class ApiDocsTestCase(APITestCase):

    def test_openapi_schema_is_served(self):
        self.assertEqual(self.client.get('/api/schema/').status_code, status.HTTP_200_OK)

    def test_swagger_ui_is_served(self):
        self.assertEqual(self.client.get('/').status_code, status.HTTP_200_OK)
