from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from ..models import Order
from .serializers import OrderSerializer, OrderStatusSerializer
from profiles_app.models import Profile

class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: List all orders where the current user is either customer or business.
    POST: Create a new order (only allowed for users with customer profile).
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the list to orders involving the current user.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def perform_create(self, serializer):
        """
        Ensure only customers can create orders.
        """
        profile = get_object_or_404(Profile, user=self.request.user)
        if profile.type != 'customer':
            raise PermissionDenied("Only customers may create orders.")
        serializer.save()

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single order (accessible to customer or business).
    PATCH: Update order status (only business user).
    DELETE: Delete order (only staff users).
    """
    queryset = Order.objects.all().select_related('offer_detail')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Use a limited serializer for PATCH (status update), full serializer otherwise.
        """
        if self.request.method == 'PATCH':
            return OrderStatusSerializer
        return OrderSerializer

    def check_object_permissions(self, request, obj):
        """
        Custom permission logic based on HTTP method and user role.
        """
        if request.method == 'GET':
            if request.user not in [obj.customer_user, obj.business_user]:
                raise PermissionDenied()
        elif request.method == 'PATCH':
            if request.user != obj.business_user:
                raise PermissionDenied()
        elif request.method == 'DELETE':
            if not request.user.is_staff:
                raise PermissionDenied()
        return super().check_object_permissions(request, obj)

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH to change status, then return full serialized order.
        """
        instance = self.get_object()
        status_serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        status_serializer.is_valid(raise_exception=True)
        self.perform_update(status_serializer)
        full_serializer = OrderSerializer(
            instance, context={'request': request}
        )
        return Response(full_serializer.data, status=status.HTTP_200_OK)
    
class OrderCountView(APIView):
    """
    GET: Return the number of in-progress orders for the given business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        biz = get_object_or_404(User, pk=business_user_id)
        count = Order.objects.filter(
            business_user=biz,
            status='in_progress'
        ).count()
        return Response({'order_count': count})
    
class CompletedOrderCountView(APIView):
    """
    GET: Return the number of completed orders for the given business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        biz = get_object_or_404(User, pk=business_user_id)
        count = Order.objects.filter(
            business_user=biz,
            status='completed'
        ).count()
        return Response({'completed_order_count': count})