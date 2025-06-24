from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for full Profile details, supporting retrieve and update.

    Exposes user-related fields as read-only.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.CharField(source='user.email',    read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user','username','first_name','last_name',
            'file','location','tel','description',
            'working_hours','type','email','created_at'
        ]
        read_only_fields = ['user','type','created_at']

class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles with limited fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user','username','first_name','last_name',
            'file','location','tel','description','working_hours','type'
        ]

class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles with minimal fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user','username','first_name','last_name',
            'file', 'type'
            # 'uploaded_at',
        ]