from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order

class OrdersAPITests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user('biz', 'biz@test.de', 'pw123')
        Profile.objects.create(user=self.biz, type='business')
        self.biz_token = Token.objects.create(user=self.biz)

        self.cust = User.objects.create_user('cust', 'cust@test.de', 'pw123')
        Profile.objects.create(user=self.cust, type='customer')
        self.cust_token = Token.objects.create(user=self.cust)

        self.offer = Offer.objects.create(
            user=self.biz,
            title='Logo Design',
            description='Wir designen Logos'
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic',
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=['Logo Design','Visitenkarten'],
            offer_type='basic'
        )

        self.order = Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            offer_detail=self.detail,
            status='in_progress'
        )

    def test_list_orders_authenticated(self):
        url = reverse('order-list')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['id'], self.order.id)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp2.data), 1)

    def test_list_orders_unauthenticated(self):
        url = reverse('order-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_as_customer(self):
        url = reverse('order-list')
        payload = {'offer_detail': self.detail.id}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        created_id = resp.data['id']
        self.assertTrue(Order.objects.filter(id=created_id).exists())
        self.assertEqual(resp.data['customer_user'], self.cust.id)
        self.assertEqual(resp.data['business_user'], self.biz.id)

    def test_create_order_as_business_forbidden(self):
        url = reverse('order-list')
        payload = {'offer_detail': self.detail.id}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        resp0 = self.client.get(url)
        self.assertEqual(resp0.status_code, status.HTTP_401_UNAUTHORIZED)

        other = User.objects.create_user('other','o@o.de','pw')
        Profile.objects.create(user=other,type='customer')
        tok_other = Token.objects.create(user=other)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {tok_other.key}')
        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data['id'], self.order.id)

    def test_patch_order_status(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cust_token.key}')
        resp_forb = self.client.patch(url, {'status':'completed'}, format='json')
        self.assertEqual(resp_forb.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp = self.client.patch(url, {'status':'completed'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')

    def test_delete_order_only_staff(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.biz_token.key}')
        resp1 = self.client.delete(url)
        self.assertEqual(resp1.status_code, status.HTTP_403_FORBIDDEN)

        admin = User.objects.create_superuser('admin','a@a.de','pw')
        tok_admin = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {tok_admin.key}')
        resp2 = self.client.delete(url)
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_order_count_endpoints(self):
        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            offer_detail=self.detail,
            status='in_progress'
        )
        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            offer_detail=self.detail,
            status='completed'
        )

        url1 = reverse('order-count', kwargs={'business_user_id': self.biz.id})
        resp1 = self.client.get(url1)
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assertEqual(resp1.data['order_count'], 2)

        url2 = reverse('completed-order-count', kwargs={'business_user_id': self.biz.id})
        resp2 = self.client.get(url2)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data['completed_order_count'], 1)