from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Profile
from .serializers import (
    ProfileSerializer,
    BusinessProfileListSerializer,
    CustomerProfileListSerializer
    )
from .permissions import IsOwnerOrReadOnly

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a user's own profile.

    Permissions:
      - Must be authenticated.
      - Only the owner can modify their profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class BusinessProfileListView(generics.ListAPIView):
    """
    List all business profiles.

    Permissions:
      - Must be authenticated.
    """
    queryset = Profile.objects.filter(type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]

class CustomerProfileListView(generics.ListAPIView):
    """
    List all customer profiles.

    Permissions:
      - Must be authenticated.
    """
    queryset = Profile.objects.filter(type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]