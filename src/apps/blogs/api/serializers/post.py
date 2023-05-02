from rest_framework import serializers

from apps.blogs.models.enums import PostStatus
from apps.users.api.serializers import UserSerializer


class PostSerializer(serializers.Serializer):
    """Post serializer."""

    id = serializers.IntegerField()  # noqa: A003
    title = serializers.CharField()
    content = serializers.CharField()  # noqa: WPS110
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=PostStatus)
    author = UserSerializer()
