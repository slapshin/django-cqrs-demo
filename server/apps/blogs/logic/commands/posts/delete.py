from dataclasses import dataclass

from apps.blogs.models import Post
from apps.core.logic import messages
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    ObjectNotFoundApplicationError,
)
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Delete post output dto."""


class Command(messages.BaseCommand[CommandResult]):
    """Delete post command."""

    user_id: int | None
    post_id: int


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Delete post command handler."""

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

        post.delete()

        return CommandResult()
