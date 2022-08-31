from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.blogs.api.serializers import PostCardSerializer
from apps.blogs.logic.queries import posts
from apps.core.api.views import BaseListQueryView


@extend_schema_serializer(component_name="PostListInput")
class _InputSerializer(serializers.Serializer):
    author = serializers.IntegerField(required=False)


class View(BaseListQueryView):
    """Posts list view."""

    query = posts.list.Query
    output_serializer = PostCardSerializer
    input_serializer = _InputSerializer

    def create_query(self) -> posts.list.Query:
        """Create query to execute."""
        input_dto = self.extract_input_dto()
        return self.query(
            author_id=input_dto.get("author"),
        )
