import pprint
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail

class OffersAPITests(APITestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user(
            username='cust', email='cust@test.de', password='pw123456'
        )
        Profile.objects.create(user=self.customer_user, type='customer')

        self.business_user = User.objects.create_user(
            username='biz', email='biz@test.de', password='pw123456'
        )
        Profile.objects.create(user=self.business_user, type='business')

        
        self.cust_token = Token.objects.create(user=self.customer_user)
        self.biz_token  = Token.objects.create(user=self.business_user)

        
        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Test Offer",
            description="A test offer"
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price=50.0,
            features=["A","B"],
            offer_type="basic"
        )

    def test_list_offers_no_auth_needed(self):
        url = reverse('offer-list-create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual(resp.data['count'], 1)
        data = resp.data['results'][0]
        self.assertEqual(data['id'], self.offer.id)
        self.assertEqual(data['min_price'], 50.0)
        self.assertEqual(data['min_delivery_time'], 3)

    def test_filter_by_creator(self):
        url = reverse('offer-list-create') + f'?user__id={self.business_user.id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        self.assertEqual(resp.data['count'], 1)
        
        url2 = reverse('offer-list-create') + f'?user__id={self.customer_user.id}'
        resp2 = self.client.get(url2)
        self.assertEqual(resp2.data['count'], 0)

    def test_create_offer_as_business(self):
        url = reverse('offer-list-create')
        payload = {
            "title": "New Offer",
            "description": "Desc",
            "details": [
                {
                    "title":"One",
                    "revisions":2,
                    "delivery_time_in_days":5,
                    "price":100,
                    "features":["X"],
                    "offer_type":"basic"
                }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp = self.client.post(url, payload, format='json')
        print("ERRORS:", pprint.pformat(resp.data))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.filter(user=self.business_user).count(), 2)
        new = Offer.objects.get(title="New Offer")
        self.assertEqual(new.details.count(), 1)

    def test_create_offer_as_customer_forbidden(self):
        url = reverse('offer-list-create')
        payload = {"title":"F","description":"D","details":[]}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_offer_requires_auth(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        resp_anon = self.client.get(url)
        self.assertEqual(resp_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], self.offer.id)

    def test_patch_offer_owner_vs_other(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
    
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp_forb = self.client.patch(url, {"title":"X"}, format='json')
        self.assertEqual(resp_forb.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp = self.client.patch(url, {"title":"Updated"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, "Updated")

    def test_delete_offer_owner_vs_other(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp_forb = self.client.delete(url)
        self.assertEqual(resp_forb.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())

    def test_get_offerdetail_no_auth(self):
        url = reverse('offerdetail-detail', kwargs={'pk': self.detail.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], self.detail.id)
        self.assertEqual(resp.data['offer_type'], 'basic')