from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Profile
from .serializers import (
    ProfileSerializer,
    BusinessProfileListSerializer,
    CustomerProfileListSerializer
    )

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

class BusinessProfileListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]

class CustomerProfileListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]