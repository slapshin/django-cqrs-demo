from django.db import transaction

from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandBus
from apps.core.logic.commands.bus import CommandInfo
from apps.core.tasks.commands import execute_command_async_task


def execute_command(command: ICommand):
    """Execute command."""
    command_bus = injector.get(ICommandBus)
    return command_bus.dispatch(command)


def execute_command_async(command: ICommand):
    """Execute command async."""
    serialized_command = command.serialize()
    command_type = type(command)

    transaction.on_commit(
        lambda: execute_command_async_task.delay(
            command_class="{0}.{1}".format(
                command_type.__module__,
                command_type.__name__,
            ),
            command_data=serialized_command,
        ),
    )


def register_commands(handlers: list[CommandInfo]):
    """Register commands handlers at injector."""
    injector.get(ICommandBus).register_many(handlers)
