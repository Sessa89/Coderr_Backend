from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
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
        return f"Review #{self.id} by {self.reviewer_id} for {self.business_user_id}"