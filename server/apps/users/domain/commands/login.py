from dataclasses import dataclass

import injector
from django.utils import timezone

from apps.core.domain import messages
from apps.core.domain.errors import AuthenticationDomainError
from apps.users.domain.interfaces import IAuthenticationService
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

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        user = self._auth_service.auth(command.username, command.password)
        if not user:
            raise AuthenticationDomainError()

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return CommandResult(
            user=user,
        )
