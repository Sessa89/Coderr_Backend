from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
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
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user','username','first_name','last_name',
            'file','location','tel','description','working_hours','type'
        ]

class CustomerProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user','username','first_name','last_name',
            'file', 'type'
            # 'uploaded_at',
        ]