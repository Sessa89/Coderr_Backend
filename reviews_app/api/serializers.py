from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Fields:
        - id: Auto-generated primary key (read-only).
        - business_user: Primary key of the user being reviewed.
        - reviewer: Primary key of the user who wrote the review (read-only).
        - rating: Integer rating between 1 and 5.
        - description: Textual description of the review.
        - created_at: Timestamp when the review was created (read-only).
        - updated_at: Timestamp when the review was last updated (read-only).
    """
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