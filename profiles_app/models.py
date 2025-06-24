from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """
    Profile model to store extended user information.

    Attributes:
        user (User): One-to-one link to Django's User.
        username (str): Redundant storage of the username for easy access.
        first_name (str): Optional first name of the user.
        last_name (str): Optional last name of the user.
        file (File): Optional uploaded file associated with the profile.
        location (str): Optional location string.
        tel (str): Optional telephone number.
        description (str): Optional free-text description.
        working_hours (str): Optional working hours string for businesses.
        type (str): Profile type, either 'customer' or 'business'.
        email (str): Contact email address.
        created_at (datetime): Timestamp when the profile was created.
    """
    TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.CharField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Profile.

        Returns:
            str: Username and profile type.
        """
        return f"{self.user.username} ({self.type})"