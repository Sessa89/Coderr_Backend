from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min

from ..models import Offer, OfferDetail
from .serializers import (
    OfferSerializer, OfferDetailSerializer, OfferCreateResponseSerializer, 
    OfferDetailURLSerializer, OfferRetrieveSerializer, OfferPatchResponseSerializer,
    OfferListSerializer
    )
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .paginations import OfferPagination
from .filters import OfferFilter

class OfferListCreateView(generics.ListCreateAPIView):
    """
    GET:
      List all offers (with filtering, search, ordering, pagination).
    POST:
      Create a new offer; only business users may create.
    """
    queryset = (Offer.objects
                .prefetch_related('details')
                .annotate(
                    min_price=Min('details__price'), 
                    min_delivery_time=Min('details__delivery_time_in_days')
                )
    )
    permission_classes = [IsBusinessUser]
    pagination_class   = OfferPagination
    filter_backends    = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferFilter
    search_fields      = ['title','description']
    ordering_fields    = ['updated_at','min_price', 'min_delivery_time']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateResponseSerializer
        return OfferListSerializer

    def create(self, request, *args, **kwargs):
        """
        Override to use the full OfferSerializer for validation,
        then return the create-response serializer.
        """
        full_serializer = OfferSerializer(data=request.data, context={'request': request})
        full_serializer.is_valid(raise_exception=True)
        self.perform_create(full_serializer)
        headers = self.get_success_headers(full_serializer.data)

        out_serializer = OfferCreateResponseSerializer(full_serializer.instance, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET:
      Retrieve a single offer (must be authenticated).
    PATCH/PUT:
      Update an offer (owner only).
    DELETE:
      Delete an offer (owner only).
    """
    queryset = Offer.objects.prefetch_related('details').all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferRetrieveSerializer
        return OfferSerializer
    
    def update(self, request, *args, **kwargs):
        """
        Override to handle nested details and return a patch-response serializer.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        full_serializer = OfferSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        full_serializer.is_valid(raise_exception=True)
        self.perform_update(full_serializer)

        out_ser = OfferPatchResponseSerializer(
            full_serializer.instance,
            context={'request': request}
        )
        return Response(out_ser.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """
    GET:
      Retrieve a single OfferDetail by ID. Public endpoint.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = []