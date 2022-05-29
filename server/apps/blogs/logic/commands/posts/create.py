from dataclasses import dataclass

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Create post output dto."""

    instance: Post


class Command(commands.BaseCommand[CommandResult]):
    """Create post command."""

    user_id: int | None
    title: str
    content: str  # noqa: WPS110
    status: PostStatus


class CommandHandler(commands.ICommandHandler[Command]):
    """Register new user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        user = User.objects.get(id=command.user_id)
        post = Post.objects.create(
            title=command.title,
            content=command.content,
            status=command.status,
            author=user,
        )

        return CommandResult(
            instance=post,
        )
