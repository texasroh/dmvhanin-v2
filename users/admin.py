from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "nickname",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )
