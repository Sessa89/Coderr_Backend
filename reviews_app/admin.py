from django.contrib import admin
from .models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'business_user',
        'reviewer',
        'rating',
        'updated_at',
    )
    list_filter = ('rating', 'business_user')
    search_fields = (
        'business_user__username',
        'reviewer__username',
        'description',
    )
    readonly_fields = ('created_at', 'updated_at')