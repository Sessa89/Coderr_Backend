from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Offer, OfferDetail
from .serializers import (
    OfferSerializer, OfferDetailSerializer, OfferCreateResponseSerializer, 
    OfferDetailURLSerializer, OfferRetrieveSerializer, OfferPatchResponseSerializer
    )
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .paginations import OfferPagination

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.prefetch_related('details').all()
    permission_classes = [IsBusinessUser]
    filter_backends    = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields   = {
        'user__id': ['exact'],
        'details__price': ['gte'],
        'details__delivery_time_in_days': ['lte'],
    }
    search_fields      = ['title','description']
    ordering_fields    = ['updated_at','min_price']
    pagination_class   = OfferPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateResponseSerializer
        return OfferSerializer

    def create(self, request, *args, **kwargs):
        full_serializer = OfferSerializer(data=request.data, context={'request': request})
        full_serializer.is_valid(raise_exception=True)
        self.perform_create(full_serializer)
        headers = self.get_success_headers(full_serializer.data)

        out_serializer = OfferCreateResponseSerializer(full_serializer.instance, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.prefetch_related('details').all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferRetrieveSerializer
        return OfferSerializer
    
    def update(self, request, *args, **kwargs):
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
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = []