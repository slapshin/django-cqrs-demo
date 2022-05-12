from django.contrib import admin


class BaseTabularInline(admin.TabularInline):
    """Base tabular inline."""

    extra = 0
    show_change_link = True
