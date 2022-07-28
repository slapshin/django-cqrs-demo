from dataclasses import dataclass

from apps.core.domain import messages
from apps.core.domain.errors import AccessDeniedDomainError


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
            raise AccessDeniedDomainError()

        return CommandResult()
