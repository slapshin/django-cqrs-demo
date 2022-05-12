from dataclasses import dataclass

from pydantic import BaseModel

from apps.core.logic import commands


class Command(BaseModel, commands.ICommand):
    """Logout command."""

    user_id: int


@dataclass(frozen=True)
class CommandResult:
    """Logout output dto."""


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Logout user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        return CommandResult()
