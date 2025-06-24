from django.db import models
from django.db.models import JSONField
from django.conf import settings

# Create your models here.

class Offer(models.Model):
    """
    Represents a high-level offer created by a business user.

    Attributes:
        user (ForeignKey): Reference to the creating user.
        title (CharField): Short title of the offer.
        image (FileField): Optional image illustrating the offer.
        description (TextField): Detailed description of the offer.
        created_at (DateTimeField): Timestamp when the offer was created.
        updated_at (DateTimeField): Timestamp when the offer was last updated.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='offers')
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='uploads/offers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a human-readable representation of an offer,
        including its title and creator username.
        """
        return f"{self.title} by {self.user.username}"

class OfferDetail(models.Model):
    """
    Represents a detailed plan or tier within an Offer,
    including pricing, delivery time, and features.

    Attributes:
        offer (ForeignKey): The parent Offer instance.
        title (CharField): Title of this detail tier (e.g., Basic).
        revisions (PositiveIntegerField): Number of revisions included.
        delivery_time_in_days (PositiveIntegerField): Delivery timeline in days.
        price (FloatField): Cost of this tier.
        features (JSONField): List of included features.
        offer_type (CharField): Classification (basic, standard, premium).
    Meta:
        Orders details by `offer_type`.
    """
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
        """
        Return a string combining the parent offer title
        and this detail's type.
        """
        return f"{self.offer.title} – {self.offer_type}"