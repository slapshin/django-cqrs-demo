from dataclasses import dataclass

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Create post output dto."""

    instance: Post


class Command(messages.BaseCommand[CommandResult]):
    """Create post command."""

    user_id: int | None
    title: str
    content: str  # noqa: WPS110
    status: PostStatus


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Register new user."""

    def execute(self, message: Command) -> CommandResult:
        """Main logic here."""
        if not message.user_id:
            raise AccessDeniedApplicationError()

        user = User.objects.get(id=message.user_id)
        post = Post.objects.create(
            title=message.title,
            content=message.content,
            status=message.status,
            author=user,
        )

        return CommandResult(
            instance=post,
        )
