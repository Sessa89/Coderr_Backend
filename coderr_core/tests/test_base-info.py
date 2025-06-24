from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews_app.models import Review
from profiles_app.models import Profile
from offers_app.models import Offer
from django.contrib.auth.models import User

class BaseInfoTests(APITestCase):
    """
    Test suite for the BaseInfoView endpoint.

    Includes tests for both non-empty and empty database states.
    """
    def setUp(self):
        """
        Create initial data for tests:
          - One business user and one customer user
          - Corresponding profiles for each user
          - One offer with two detail options (basic and premium)
          - One review for the business user
        """
        self.biz_user = User.objects.create_user('biz', 'biz@example.com', 'pass')
        Profile.objects.create(user=self.biz_user, type='business')
    
        self.cust_user = User.objects.create_user('cust', 'cust@example.com', 'pass')
        Profile.objects.create(user=self.cust_user, type='customer')

        self.offer = Offer.objects.create(
            user=self.biz_user,
            title='Test Offer',
            description='Desc'
        )
        self.offer.details.create(
            title='A', revisions=1, delivery_time_in_days=5,
            price=100, features=['X'], offer_type='basic'
        )
        self.offer.details.create(
            title='B', revisions=1, delivery_time_in_days=3,
            price=200, features=['Y'], offer_type='premium'
        )

        Review.objects.create(
            business_user=self.biz_user,
            reviewer=self.cust_user,
            rating=4,
            description='Gut'
        )

    def test_base_info_counts(self):
        """
        Verify that the endpoint returns correct counts when data exists.

        Expected response fields:
            - review_count = 1
            - average_rating = 4.0
            - business_profile_count = 1
            - offer_count = 1
        """
        url = reverse('base-info')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(data['review_count'], 1)
        self.assertEqual(data['average_rating'], 4.0)
        self.assertEqual(data['business_profile_count'], 1)
        self.assertEqual(data['offer_count'], 1)

    def test_base_info_empty(self):
        """
        Verify that the endpoint returns zero values when no data is present.

        Expected response payload:
            {'review_count': 0, 'average_rating': 0.0,
             'business_profile_count': 0, 'offer_count': 0}
        """
        Review.objects.all().delete()
        Offer.objects.all().delete()
        Profile.objects.filter(type='business').delete()

        url = reverse('base-info')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(data, {
            'review_count': 0,
            'average_rating': 0.0,
            'business_profile_count': 0,
            'offer_count': 0,
        })