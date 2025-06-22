from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']