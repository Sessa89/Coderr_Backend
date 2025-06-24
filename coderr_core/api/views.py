from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from reviews_app.models import Review
from profiles_app.models import Profile
from offers_app.models import Offer

class BaseInfoView(APIView):
    """
    API view to retrieve core statistics about the platform.

    Provides the total number of reviews, the average rating across all reviews,
    the count of business profiles, and the total count of offers.
    """
    permission_classes = []

    def get(self, request):
        """
        Handle GET requests and return aggregated base information.

        Returns a JSON response containing:
            - review_count: Total number of reviews in the system.
            - average_rating: Average rating value, rounded to one decimal place.
            - business_profile_count: Number of profiles marked as 'business'.
            - offer_count: Total number of offers created.

        If no reviews exist, the average rating defaults to 0.0.
        """
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        
        average_rating = round(average_rating, 1)
        business_profile_count = Profile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()
        return Response({
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        })