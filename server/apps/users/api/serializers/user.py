from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """User serializer."""

    id = serializers.IntegerField()  # noqa: A003
    email = serializers.CharField()
