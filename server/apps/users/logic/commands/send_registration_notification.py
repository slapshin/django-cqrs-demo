from dataclasses import dataclass

import injector

from apps.core.logic import messages
from apps.core.logic.errors import ObjectNotFoundApplicationError
from apps.core.logic.interfaces import IEMailService
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Send registration notification output dto."""


class Command(messages.BaseCommand[CommandResult]):
    """Send registration notification command."""

    user_id: int


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Send registration notification command handler."""

    @injector.inject
    def __init__(self, email_service: IEMailService) -> None:
        """Initialize."""
        self._email_service = email_service

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        try:
            user = User.objects.filter(id=command.user_id).first()
        except User.DoesNotExist:
            raise ObjectNotFoundApplicationError()

        self._email_service.send_email(
            "Successful registration",
            "You have successfully registered",
            user.email,
        )

        return CommandResult()
