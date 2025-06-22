from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User

from ..models import Review
from .serializers import ReviewSerializer
from profiles_app.models import Profile

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if 'business_user_id' in params:
            qs = qs.filter(business_user__id=params['business_user_id'])
        if 'reviewer_id' in params:
            qs = qs.filter(reviewer__id=params['reviewer_id'])
        ord = params.get('ordering')
        if ord in ('rating', 'updated_at'):
            qs = qs.order_by(ord)
        return qs

    def perform_create(self, serializer):
        user = self.request.user

        profile = get_object_or_404(Profile, user=user)
        if profile.type != 'customer':
            raise PermissionDenied("Only customers are able to create reviews.")
        bu = serializer.validated_data['business_user']
        
        if Review.objects.filter(business_user=bu, reviewer=user).exists():
            raise ValidationError("You have already rated this business.")
        serializer.save(reviewer=user)

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def check_object_permissions(self, request, obj):
        if request.method in ('PATCH', 'DELETE') and request.user != obj.reviewer:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().check_object_permissions(request, obj)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        inst = self.get_object()
        self.check_object_permissions(request, inst)
        inst.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)