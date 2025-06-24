from django.contrib import admin
from django.db.models import Min
from .models import Offer, OfferDetail

# Register your models here.

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 1
    verbose_name = "Angebotsdetail"
    verbose_name_plural = "Angebotsdetails"

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'min_price',
        'min_delivery_time',
        'created_at',
        'updated_at',
    )
    list_select_related = ('user',)
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('user',)
    inlines = (OfferDetailInline,)

    def min_price(self, obj):
        return obj.details.aggregate(Min('price'))['price__min'] or 0
    min_price.short_description = 'Mindestpreis'

    def min_delivery_time(self, obj):
        return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0
    min_delivery_time.short_description = 'Min. Lieferzeit (Tage)'

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'offer',
        'offer_type',
        'title',
        'price',
        'delivery_time_in_days',
        'revisions',
    )
    list_filter = ('offer_type',)
    search_fields = ('title', 'offer__title')