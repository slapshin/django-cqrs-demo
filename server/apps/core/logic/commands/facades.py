from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandBus
from apps.core.logic.commands.bus import CommandInfo


def execute_command(command: ICommand):
    """Execute query."""
    command_bus = injector.get(ICommandBus)
    return command_bus.dispatch(command)


def register_commands(handlers: list[CommandInfo]):
    """Register commands handlers at injector."""
    injector.get(ICommandBus).register_many(handlers)
