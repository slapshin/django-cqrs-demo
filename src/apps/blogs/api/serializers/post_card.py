from rest_framework import serializers

from apps.users.api.serializers import UserSerializer


class PostCardSerializer(serializers.Serializer):
    """Post card serializer."""

    id = serializers.IntegerField()  # noqa: A003
    title = serializers.CharField()
    author = UserSerializer()
