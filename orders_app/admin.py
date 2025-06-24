from django.contrib import admin
from .models import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_user',
        'business_user',
        'offer_detail',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'business_user')
    search_fields = (
        'customer_user__username',
        'business_user__username',
        'offer_detail__title',
    )
    readonly_fields = ('created_at', 'updated_at')