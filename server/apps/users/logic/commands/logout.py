from dataclasses import dataclass

from pydantic import BaseModel

from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError


class Command(BaseModel, commands.ICommand):
    """Logout command."""

    user_id: int | None


@dataclass(frozen=True)
class CommandResult:
    """Logout output dto."""


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Logout user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        return CommandResult()
