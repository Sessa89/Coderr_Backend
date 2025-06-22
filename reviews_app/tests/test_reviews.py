from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from profiles_app.models import Profile
from reviews_app.models import Review
import datetime

class ReviewsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.business1 = User.objects.create_user(username='biz1', password='pw')
        self.business2 = User.objects.create_user(username='biz2', password='pw')
        self.customer1 = User.objects.create_user(username='cust1', password='pw')
        self.customer2 = User.objects.create_user(username='cust2', password='pw')

        Profile.objects.create(user=self.business1, type='business')
        Profile.objects.create(user=self.business2, type='business')
        Profile.objects.create(user=self.customer1, type='customer')
        Profile.objects.create(user=self.customer2, type='customer')

        now = timezone.now()
        self.rev1 = Review.objects.create(
            business_user=self.business1,
            reviewer=self.customer1,
            rating=4,
            description="Good service",
            created_at=now - datetime.timedelta(days=2),
            updated_at=now - datetime.timedelta(days=2),
        )
        self.rev2 = Review.objects.create(
            business_user=self.business2,
            reviewer=self.customer1,
            rating=5,
            description="Excellent!",
            created_at=now - datetime.timedelta(days=1),
            updated_at=now - datetime.timedelta(days=1),
        )
        self.rev3 = Review.objects.create(
            business_user=self.business1,
            reviewer=self.customer2,
            rating=3,
            description="Okay",
            created_at=now,
            updated_at=now,
        )

    def test_list_reviews_requires_auth(self):
        url = '/api/reviews/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reviews(self):
        url = '/api/reviews/'
        self.client.force_authenticate(self.customer1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(resp.data), 3)

    def test_filter_by_business_user(self):
        url = f'/api/reviews/?business_user_id={self.business1.id}'
        self.client.force_authenticate(self.customer2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(resp.data), 2)
        for item in resp.data:
            self.assertEqual(item['business_user'], self.business1.id)

    def test_filter_by_reviewer(self):
        url = f'/api/reviews/?reviewer_id={self.customer1.id}'
        self.client.force_authenticate(self.customer2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual({r['id'] for r in resp.data}, {self.rev1.id, self.rev2.id})

    def test_ordering_by_rating(self):
        url = '/api/reviews/?ordering=rating'
        self.client.force_authenticate(self.customer1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        ratings = [r['rating'] for r in resp.data]
        self.assertEqual(ratings, sorted(ratings))

    def test_retrieve_review(self):
        url = f'/api/reviews/{self.rev1.id}/'
        
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.force_authenticate(self.business2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], self.rev1.id)

    def test_create_review_as_customer(self):
        url = '/api/reviews/'
        payload = {
            'business_user': self.business2.id,
            'rating': 5,
            'description': "Top!"
        }
        self.client.force_authenticate(self.customer2)
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['reviewer'], self.customer2.id)
        self.assertEqual(resp.data['business_user'], self.business2.id)

    def test_create_review_as_business_forbidden(self):
        url = '/api/reviews/'
        payload = {
            'business_user': self.business1.id,
            'rating': 4,
            'description': "Nice"
        }
        self.client.force_authenticate(self.business2)
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_duplicate_review(self):
        url = '/api/reviews/'
        payload = {
            'business_user': self.business1.id,
            'rating': 5,
            'description': "Again"
        }
        
        self.client.force_authenticate(self.customer1)
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_as_reviewer(self):
        url = f'/api/reviews/{self.rev1.id}/'
        payload = {'rating': 1, 'description': "Bad"}
        self.client.force_authenticate(self.customer1)
        resp = self.client.patch(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['rating'], 1)
        self.assertEqual(resp.data['description'], "Bad")

    def test_update_review_as_other_forbidden(self):
        url = f'/api/reviews/{self.rev1.id}/'
        payload = {'rating': 2}
        self.client.force_authenticate(self.customer2)
        resp = self.client.patch(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_as_reviewer(self):
        url = f'/api/reviews/{self.rev1.id}/'
        self.client.force_authenticate(self.customer1)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertFalse(Review.objects.filter(id=self.rev1.id).exists())

    def test_delete_review_as_other_forbidden(self):
        url = f'/api/reviews/{self.rev2.id}/'
        self.client.force_authenticate(self.customer2)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)