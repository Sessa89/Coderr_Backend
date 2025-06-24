from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from profiles_app.models import Profile

class RegistrationTests(APITestCase):
    """
    Test cases for user registration functionality.
    """
    def setUp(self):
        self.url = reverse('registration')

    def test_registration_success(self):
        """
        Valid signup data returns HTTP 201 and creates User and Profile.
        """
        payload = {
            "username": "Max Mustermann",
            "email": "max-mustermann@test.de",
            "password": "strongpass123",
            "repeated_password": "strongpass123",
            "type": "customer"
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], payload['username'])
        self.assertEqual(response.data['email'], payload['email'])
        self.assertTrue(isinstance(response.data['user_id'], int))

        user = User.objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.type, payload['type'])

    def test_registration_password_mismatch(self):
        """
        Mismatched passwords should return HTTP 400 with error on 'password'.
        """
        payload={
            "username": "Max Mustermann",
            "email": "max-mustermann@test.de",
            "password": "strongpass123",
            "repeated_password": "wrongpass",
            "type": "customer"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_duplicate_username(self):
        """
        Duplicate username should return HTTP 400 with error on 'username'.
        """
        User.objects.create_user(username='John Doe', email='john_doe@test.de', password='pw123456')
        payload = {
            "username": "John Doe",
            "email": "other@example.com",
            "password": "newpass123",
            "repeated_password": "newpass123",
            "type": "business"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_duplicate_email(self):
        """
        Duplicate email should return HTTP 400 with error on 'email'.
        """
        User.objects.create_user(username='Max Mustermann', email='max-mustermann@test.de', password='strongpass123')
        payload = {
            "username": "John Doe",
            "email": "max-mustermann@test.de",
            "password": "newpass123",
            "repeated_password": "newpass123",
            "type": "business"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)