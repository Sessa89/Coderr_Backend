from django.db import models
from django.db.models import ProtectedError
from django.urls import reverse
from rest_framework import serializers

from ..models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail, used for nested create/update and full detail view.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]

class OfferSerializer(serializers.ModelSerializer):
    """
    Core serializer for Offer, handling nested details,
    creation and update of related OfferDetail instances.
    """
    user              = serializers.PrimaryKeyRelatedField(read_only=True)
    details           = OfferDetailSerializer(many=True)
    min_price         = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = [
            'id','user','title','image','description',
            'created_at','updated_at',
            'details','min_price','min_delivery_time',
        ]
        read_only_fields = ['user','created_at','updated_at']

    def create(self, validated_data):
        """
        Override to handle creating nested OfferDetail instances after
        creating the Offer itself.
        """
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for det in details_data:
            OfferDetail.objects.create(offer=offer, **det)
        return offer

    def update(self, instance, validated_data):
        """
        Override to handle updating and synchronizing nested details:
        - Update existing details by ID.
        - Create new details if ID not provided.
        - Delete details omitted from the update payload.
        """
        details_data = validated_data.pop('details', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if details_data is not None:
            existing = {d.id: d for d in instance.details.all()}
            for det in details_data:
                det_id = det.get('id', None)
                if det_id and det_id in existing:
                    obj = existing.pop(det_id)
                    for k,v in det.items():
                        if k!='id':
                            setattr(obj, k, v)
                    obj.save()
                else:
                    OfferDetail.objects.create(offer=instance, **det)
            for obj in existing.values():
                try:
                    obj.delete()
                except ProtectedError as e:
                    raise serializers.ValidationError({
                        'details': f"Cannot delete detail #{obj.pk}: {str(e)}"
                    })
        return instance
    
class OfferCreateResponseSerializer(serializers.ModelSerializer):
    """
    Serializer used to return data on offer creation requests,
    matching the nested input structure.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details',]

class OfferDetailURLSerializer(serializers.ModelSerializer):
    """
    Serializer that provides URLs for each OfferDetail instance.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """
        Build fully-qualified URL for the OfferDetail detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('offerdetail-detail', kwargs={'pk': obj.pk})
        )

class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single Offer,
    returning detail URLs instead of full nested details.
    """
    created_at         = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at         = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    details            = OfferDetailURLSerializer(many=True, read_only=True)
    min_price          = serializers.ReadOnlyField()
    min_delivery_time  = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time',
        ]
        read_only_fields = fields
  
class OfferPatchResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for patch requests on Offer,
    returning full nested details on response.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Offer instances,
    including user summary fields and detail URLs.
    """
    created_at         = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at         = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    details            = OfferDetailURLSerializer(many=True, read_only=True)
    min_price          = serializers.ReadOnlyField()
    min_delivery_time  = serializers.ReadOnlyField()
    user_details       = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details',
        ]
        read_only_fields = fields

    def get_user_details(self, obj):
        """
        Return a summary of the creating user's profile
        (first name, last name, username).
        """
        return {
            'first_name': obj.user.first_name,
            'last_name':  obj.user.last_name,
            'username':   obj.user.username,
        }