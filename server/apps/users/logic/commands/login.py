from dataclasses import dataclass

from django.contrib.auth import authenticate
from pydantic import BaseModel

from apps.core.logic import commands
from apps.users.models import User


class Command(BaseModel, commands.ICommand):
    """Login command."""

    username: str
    password: str


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    user: User


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Register new user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        user = authenticate(
            username=command.username,
            password=command.password,
        )
        if user is None:
            raise ValueError("Invalid username or password.")

        return CommandResult(
            user=user,
        )
