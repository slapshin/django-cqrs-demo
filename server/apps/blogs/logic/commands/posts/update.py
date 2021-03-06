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


class Command(messages.BaseCommand[CommandResult]):
    """Create post command."""

    user_id: int | None
    post_id: int
    title: str
    content: str  # noqa: WPS110
    status: PostStatus


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Register new user."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        user = User.objects.get(id=command.user_id)

        try:
            post = Post.objects.get(id=command.post_id)
        except Post.DoesNotExist:
            raise ObjectNotFoundApplicationError()

        if post.author != user:
            raise AccessDeniedApplicationError()

        post.title = command.title
        post.content = command.content
        post.status = command.status
        post.save()

        return CommandResult(
            instance=post,
        )
