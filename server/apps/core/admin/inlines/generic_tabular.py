from django.contrib.contenttypes.admin import GenericTabularInline


class BaseGenericTabularInline(GenericTabularInline):
    """Base generic tabular inline."""

    extra = 0
    show_change_link = True
