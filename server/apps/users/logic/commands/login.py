from dataclasses import dataclass

import injector
from django.utils import timezone

from apps.core.logic import messages
from apps.core.logic.errors import AuthenticationApplicationError
from apps.users.logic.interfaces import IAuthenticationService
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    user: User


class Command(messages.BaseCommand[CommandResult]):
    """Login command."""

    username: str
    password: str


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Register new user."""

    @injector.inject
    def __init__(self, auth_service: IAuthenticationService) -> None:
        """Initializing."""
        self._auth_service = auth_service

    def execute(self, message: Command) -> CommandResult:
        """Main logic here."""
        user = self._auth_service.auth(message.username, message.password)
        if not user:
            raise AuthenticationApplicationError()

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return CommandResult(
            user=user,
        )
