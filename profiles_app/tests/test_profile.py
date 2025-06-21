from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile

class ProfilesAPITests(APITestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user(
            username='Customer 1', email='customer1@test.de', password='customerpw'
        )
        self.business_user = User.objects.create_user(
            username='Business 1', email='business1@test.de', password='bizpass'
        )
        
        self.customer_profile = Profile.objects.create(
            user=self.customer_user, type='customer'
        )
        self.business_profile = Profile.objects.create(
            user=self.business_user, type='business',
            first_name='Max', last_name='Mustermann',
            location='Berlin', tel='0123456789',
            description='Business description', working_hours='9-17'
        )
        
        self.customer_token    = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)

    def test_get_own_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.customer_profile.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['user'], self.customer_user.id)
        self.assertEqual(resp.data['type'], 'customer')

    def test_cannot_get_other_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.business_profile.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.business_profile.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "location": "Hamburg",
            "tel": "0987654321",
            "description": "Updated desc",
            "working_hours": "10-18"
        }
        resp = self.client.patch(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.business_profile.refresh_from_db()
        self.assertEqual(self.business_profile.first_name, "John")
        self.assertEqual(self.business_profile.location, "Hamburg")

    def test_list_business_profiles(self):
        url = reverse('business-profiles')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['user'], self.business_user.id)

    def test_list_customer_profiles(self):
        url = reverse('customer-profiles')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['user'], self.customer_user.id)
        self.assertEqual(resp.data[0]['type'], 'customer')

    def test_unauthenticated_access(self):
        urls = [
            reverse('profile-detail',      kwargs={'pk': self.customer_profile.pk}),
            reverse('business-profiles'),
            reverse('customer-profiles'),
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)