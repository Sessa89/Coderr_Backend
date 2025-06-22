from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from reviews_app.models import Review
from profiles_app.models import Profile
from offers_app.models import Offer

class BaseInfoView(APIView):
    permission_classes = []

    def get(self, request):
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