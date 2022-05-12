from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    """Base model admin."""

    list_per_page = 20
