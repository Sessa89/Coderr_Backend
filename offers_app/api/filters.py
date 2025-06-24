import django_filters
from django.db.models import Min

from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    creator_id        = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price         = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']

    def queryset(self):
        base_queryset = super().queryset
        return base_queryset.annotate(
            min_price=Min('details__price'), 
            min_delivery_time=Min('details__delivery_time_in_days')
        )

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.filter(min_delivery_time__lte=value)