from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
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
        return f"{self.user.username} ({self.type})"