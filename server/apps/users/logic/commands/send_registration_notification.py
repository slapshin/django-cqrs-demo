from dataclasses import dataclass

import injector

from apps.core.logic import commands
from apps.core.logic.errors import ObjectNotFoundApplicationError
from apps.core.logic.interfaces import IEMailService
from apps.users.models import User


class Command(commands.BaseCommand):
    """Send registration notification command."""

    user_id: int


@dataclass(frozen=True)
class CommandResult:
    """Send registration notification output dto."""


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Send registration notification command handler."""

    @injector.inject
    def __init__(self, email_service: IEMailService):
        """Initialize."""
        self._email_service = email_service

    def execute(self, command: Command) -> CommandResult:
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
