from django.db import models
from django.urls import reverse
from rest_framework import serializers

from ..models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
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
    user              = serializers.PrimaryKeyRelatedField(read_only=True)
    details           = OfferDetailSerializer(many=True)
    min_price         = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id','user','title','image','description',
            'created_at','updated_at',
            'details','min_price','min_delivery_time',
        ]
        read_only_fields = ['user','created_at','updated_at']

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for det in details_data:
            OfferDetail.objects.create(offer=offer, **det)
        return offer

    def update(self, instance, validated_data):
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
                obj.delete()
        return instance
    
class OfferCreateResponseSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

class OfferDetailURLSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('offerdetail-detail', kwargs={'pk': obj.pk})
        )

class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailURLSerializer(many=True, read_only=True)
    min_price         = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details',
            'min_price', 'min_delivery_time',
        ]
        read_only_fields = fields

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0
    
class OfferPatchResponseSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]