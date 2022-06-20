from dataclasses import dataclass

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    ObjectNotFoundApplicationError,
)
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Create post output dto."""

    instance: Post


class Command(messages.BaseMessage[CommandResult]):
    """Create post command."""

    user_id: int | None
    post_id: int
    title: str
    content: str  # noqa: WPS110
    status: PostStatus


class CommandHandler(messages.IMessageHandler[Command]):
    """Register new user."""

    def execute(self, message: Command) -> CommandResult:
        """Main logic here."""
        if not message.user_id:
            raise AccessDeniedApplicationError()

        user = User.objects.get(id=message.user_id)

        try:
            post = Post.objects.get(id=message.post_id)
        except Post.DoesNotExist:
            raise ObjectNotFoundApplicationError()

        if post.author != user:
            raise AccessDeniedApplicationError()

        post.title = message.title
        post.content = message.content
        post.status = message.status
        post.save()

        return CommandResult(
            instance=post,
        )
