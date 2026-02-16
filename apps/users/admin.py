# Django modules
from django.contrib.admin import register, ModelAdmin

# Project modules
from apps.users.models import CustomUser

@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """Admin model for CustomUser"""

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )

    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering =("date_joined",)