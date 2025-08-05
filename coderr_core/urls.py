"""
URL configuration for coderr_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user_auth_app.api.views import RegistrationView, CustomLoginView
from profiles_app.api.views import ProfileDetailView, BusinessProfileListView, CustomerProfileListView
from offers_app.api.views import OfferListCreateView, OfferRetrieveUpdateDestroyView, OfferDetailRetrieveView
from orders_app.api.views import OrderListCreateView, OrderRetrieveUpdateDestroyView, OrderCountView, CompletedOrderCountView
from reviews_app.api.views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView
from coderr_core.api.views import BaseInfoView

from django.conf.urls.static import static
from coderr_core import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/registration/', RegistrationView.as_view(), name='registration'),
    path('api/login/', CustomLoginView.as_view(), name='login'),

    path('api/profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('api/profiles/business/', BusinessProfileListView.as_view(), name='business-profiles'),
    path('api/profiles/customer/', CustomerProfileListView.as_view(), name='customer-profiles'),

    path('api/offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('api/offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-detail'),
    path('api/offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offerdetail-detail'),

    path('api/orders/', OrderListCreateView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('api/order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('api/completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),

    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),

    path('api/base-info/', BaseInfoView.as_view(), name='base-info'),
] + staticfiles_urlpatterns()
