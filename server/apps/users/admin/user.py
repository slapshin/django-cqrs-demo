from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """User admin."""

    list_display = (
        "email",
        "last_login",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_active", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    exclude = ("user_permissions",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "last_login",
                ),
            },
        ),
    )
    readonly_fields = ("last_login",)
