from django.db import models
from django.db.models import JSONField
from django.conf import settings

# Create your models here.

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='offers')
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='uploads/offers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class OfferDetail(models.Model):
    OFFER_TYPES = [
        ('basic',   'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )
    title = models.CharField(max_length=200)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.FloatField()
    features = JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    class Meta:
        ordering = ['offer_type']

    def __str__(self):
        return f"{self.offer.title} – {self.offer_type}"