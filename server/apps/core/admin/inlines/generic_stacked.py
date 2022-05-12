from django.contrib.contenttypes.admin import GenericStackedInline


class BaseGenericStackedInline(GenericStackedInline):
    """Base generic stacked inline."""

    extra = 0
    show_change_link = True
