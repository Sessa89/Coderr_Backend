from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
    """
    Model representing a review written by a customer for a business.

    Fields:
        - business_user: ForeignKey to User being reviewed.
        - reviewer:    ForeignKey to User who wrote the review.
        - rating:      Integer between 1 and 5, enforced by validators.
        - description: Textual content of the review.
        - created_at:  Timestamp when the review was first created.
        - updated_at:  Timestamp when the review was last modified.
    """
    business_user = models.ForeignKey(
        User,
        related_name='reviews_received',
        on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        User,
        related_name='reviews_made',
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
        ordering = ['-updated_at']

    def __str__(self):
        """
        String representation showing review ID and involved user IDs.
        """
        return f"Review #{self.id} by {self.reviewer_id} for {self.business_user_id}"