from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.blogs.api.serializers import PostSerializer
from apps.blogs.logic.commands import posts
from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.api.views import BaseCommandView


@extend_schema_serializer(component_name="PostUpdateInput")
class _InputSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()  # noqa: WPS110
    status = serializers.ChoiceField(choices=PostStatus)


class View(BaseCommandView):
    """Post update view."""

    command = posts.update.Command
    input_serializer = _InputSerializer
    output_serializer = PostSerializer

    def create_command(self) -> posts.update.Command:
        """Create command to execute."""
        input_dto = self.extract_input_dto()
        return self.command(
            user_id=self.user.id if self.user else None,
            post_id=self.kwargs["pk"],
            title=input_dto["title"],
            content=input_dto["content"],
            status=input_dto["status"],
        )

    def get_output_serializer_instance(
        self,
        command_result: posts.update.CommandResult,
    ) -> Post:
        """Get output serializer instance."""
        return command_result.instance
