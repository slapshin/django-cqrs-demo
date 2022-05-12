from dataclasses import dataclass

from pydantic import BaseModel

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.models import User


class Command(BaseModel, commands.ICommand):
    """Create post command."""

    user_id: int | None
    title: str
    content: str
    status: PostStatus


@dataclass(frozen=True)
class CommandResult:
    """Create post output dto."""

    instance: Post


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
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
