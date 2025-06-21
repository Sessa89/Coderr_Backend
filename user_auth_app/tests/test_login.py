from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class LoginTests(APITestCase):
    def setUp(self):
        self.url = reverse('login')

        self.username = "Max Mustermann"
        self.password = "strongpass123"
        self.email = "max-mustermann@test.de"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_login_success(self):
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['email'], self.email)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_invalid_password(self):
        payload = {
            "username": self.username,
            "password": "wrongpass"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        payload = {
            "username": "Jane Doe",
            "password": "forgotpw"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)