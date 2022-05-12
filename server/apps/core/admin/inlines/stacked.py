from django.contrib import admin



class BaseStackedInline(admin.StackedInline):
    """Base stacked inline."""

    extra = 0
    show_change_link = True
