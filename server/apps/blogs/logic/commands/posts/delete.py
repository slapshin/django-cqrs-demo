from dataclasses import dataclass

from pydantic import BaseModel

from apps.blogs.models import Post
from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError, ObjectNotFoundError
from apps.users.models import User


class Command(BaseModel, commands.ICommand):
    """Delete post command."""

    user_id: int | None
    post_id: int


@dataclass(frozen=True)
class CommandResult:
    """Delete post output dto."""


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Delete post command handler."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        user = User.objects.get(id=command.user_id)

        try:
            post = Post.objects.get(id=command.post_id)
        except Post.DoesNotExist:
            raise ObjectNotFoundError()

        if post.author != user:
            raise AccessDeniedApplicationError()

        post.delete()

        return CommandResult()
