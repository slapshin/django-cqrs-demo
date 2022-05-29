from dataclasses import dataclass

from django.contrib.auth import authenticate

from apps.core.logic import commands
from apps.core.logic.errors import AuthenticationApplicationError
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    user: User


class Command(commands.BaseCommand[CommandResult]):
    """Login command."""

    username: str
    password: str


class CommandHandler(commands.ICommandHandler[Command]):
    """Register new user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        user = authenticate(
            username=command.username,
            password=command.password,
        )
        if user is None:
            raise AuthenticationApplicationError()

        return CommandResult(
            user=user,
        )
