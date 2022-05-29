from dataclasses import dataclass

from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError


@dataclass(frozen=True)
class CommandResult:
    """Logout output dto."""


class Command(commands.BaseCommand[CommandResult]):
    """Logout command."""

    user_id: int | None


class CommandHandler(commands.ICommandHandler[Command]):
    """Logout user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        return CommandResult()
