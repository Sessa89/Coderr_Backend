import django_filters
from django.db.models import Min

from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    """
    FilterSet for the Offer model.

    Filters:
        creator_id: exact match on the creating user ID.
        user__id: exact match on the user ID.
        min_price: filter offers with any detail price >= value.
        max_delivery_time: filter offers with any detail delivery time <= value.
    """
    creator_id        = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    user__id          = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price         = django_filters.NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['user__id', 'min_price', 'max_delivery_time']

    def queryset(self):
        """
        Annotate the base queryset with the minimum price and
        minimum delivery time across related details.
        """
        base_queryset = super().queryset
        return base_queryset.annotate(
            min_price=Min('details__price'), 
            min_delivery_time=Min('details__delivery_time_in_days')
        )

    def filter_min_price(self, queryset, name, value):
        """
        Apply filter to include only offers where the annotated
        minimum price is >= the specified value.
        """
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Apply filter to include only offers where the annotated
        minimum delivery time is <= the specified value.
        """
        return queryset.filter(min_delivery_time__lte=value)