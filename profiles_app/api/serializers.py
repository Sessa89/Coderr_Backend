from rest_framework import serializers
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for full Profile details, supporting retrieve and update.

    Exposes user-related fields as read-only.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]
        read_only_fields = ['user', 'type', 'created_at']

    def update(self, instance, validated_data):
        """
        Override the default update to allow updating the related User’s email address.

            - Extracts any ‘email’ value from the nested ‘user’ data.
            - Calls the superclass to update the Profile fields.
            - If a new email was provided, assigns it to instance.user.email and saves the User.
        """
        user_data = validated_data.pop('user', {})
        instance = super().update(instance, validated_data)
        new_email = user_data.get('email')
        if new_email:
            instance.user.email = new_email
            instance.user.save()
        return instance


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles with limited fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description', 'working_hours', 'type'
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles with minimal fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'type'
            # 'uploaded_at',
        ]
