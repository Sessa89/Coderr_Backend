from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles_app.models import Profile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Ensures unique username and email, matches passwords, and creates a Profile.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This username is already taken.'
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already taken.'
            )
        ]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """
        Check that password and repeated_password match.
        """
        if data['password'] != data.pop('repeated_password'):
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        return data

    def create(self, validated_data):
        """
        Create a new User and associated Profile with the given type.
        """
        user_type = validated_data.pop('type')
        account = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=account, type=user_type)
        
        return account

class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in an existing user.
    Validates that the username exists and password is correct.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Authenticate the user by username and password.
        Raises ValidationError if credentials are invalid.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                account = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("This account does not exist.")

            if not account.check_password(password):
                raise serializers.ValidationError("Log in failed. Check your entered username and password.")
        else:
            raise serializers.ValidationError("Username and password are required.")

        attrs['user'] = account
        return attrs