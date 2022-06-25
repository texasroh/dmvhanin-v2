from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "nickname",
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
        "google_id",
        "kakao_id",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("nickname",)},
        ),
        (
            "email verification",
            {
                "fields": (
                    "email_verified",
                    "email_secret",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    search_fields = ("email", "nickname")
    ordering = (
        "-is_superuser",
        "-is_staff",
        "email",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
