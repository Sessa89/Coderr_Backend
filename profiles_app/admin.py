from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'type',
        'first_name',
        'last_name',
        'location',
        'tel',
    )
    list_filter = ('type',)
    search_fields = (
        'user__username',
        'first_name',
        'last_name',
        'location',
    )