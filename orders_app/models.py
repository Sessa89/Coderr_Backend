from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User,
        related_name='customer_orders',
        on_delete=models.CASCADE
    )
    business_user = models.ForeignKey(
        User,
        related_name='business_orders',
        on_delete=models.CASCADE
    )
    offer_detail = models.ForeignKey(
        'offers_app.OfferDetail',
        on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.offer_detail.title} ({self.status})"