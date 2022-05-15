from rest_framework import serializers


class PaginationMixin(serializers.Serializer):
    """Mixin for pagination fields."""

    page_size = serializers.IntegerField(required=False, min_value=1)
    page = serializers.IntegerField(required=False, min_value=0)
