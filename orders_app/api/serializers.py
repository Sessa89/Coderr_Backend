from rest_framework import serializers
from ..models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order objects.

    - Read-only fields include customer_user, business_user, and all offer_detail-derived fields.
    - Write-only field 'offer_detail_id' is used to select the related OfferDetail.
    """
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Order._meta.get_field('offer_detail').remote_field.model.objects.all(),
        source='offer_detail',
        write_only=True
    )
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source='offer_detail.delivery_time_in_days', read_only=True
    )
    price = serializers.DecimalField(
        source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True
    )
    features = serializers.ListField(
        source='offer_detail.features', child=serializers.CharField(), read_only=True
    )
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'offer_detail_id',
            'title', 'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title',
            'revisions', 'delivery_time_in_days', 'price',
            'features','offer_type', 'created_at','updated_at'
        ]

    def create(self, validated_data):
        """
        Create a new Order instance.

        - Automatically assigns the requesting user as the customer_user.
        - Determines business_user from the offer_detail's related Offer.
        """
        user = self.context['request'].user
        detail = validated_data.pop('offer_detail')
        
        validated_data['customer_user'] = user
        validated_data['business_user'] = detail.offer.user
        order = Order.objects.create(offer_detail=detail, **validated_data)
        return order

class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only the status field of an Order.
    """
    class Meta:
        model = Order
        fields = ['status']