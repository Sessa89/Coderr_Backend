from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    """
    Represents an order placed by a customer for a specific offer detail.

    Attributes:
        customer_user (ForeignKey): The user who placed the order.
        business_user (ForeignKey): The business user fulfilling the order.
        offer_detail (ForeignKey): The specific offer configuration for this order.
        status (CharField): Current status of the order (in_progress, completed, cancelled).
        created_at (DateTimeField): Timestamp when the order was created.
        updated_at (DateTimeField): Timestamp when the order was last updated.
    """
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
        """
        Return a human-readable representation of the order.
        """
        return f"Order #{self.id} - {self.offer_detail.title} ({self.status})"