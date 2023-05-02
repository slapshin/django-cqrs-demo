from dataclasses import dataclass

from apps.core.logic import messages
from apps.core.logic.errors import AccessDeniedApplicationError


@dataclass(frozen=True)
class CommandResult:
    """Logout output dto."""


class Command(messages.BaseCommand[CommandResult]):
    """Logout command."""

    user_id: int | None


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Logout user."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        if not command.user_id:
            raise AccessDeniedApplicationError()

        return CommandResult()
