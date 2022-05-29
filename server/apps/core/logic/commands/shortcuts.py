import typing as ty

from django.db import transaction

from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandBus
from apps.core.logic.commands.bus import TCommandHandler
from apps.core.logic.commands.handler import TCommandResult
from apps.core.tasks.commands import execute_command_async_task


def execute_command(command: ICommand[TCommandResult]) -> TCommandResult:
    """Execute command."""
    command_bus = injector.get(ICommandBus)
    return command_bus.dispatch(command)


def execute_command_async(command: ICommand) -> None:
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


def register_commands(handlers: ty.Iterable[ty.Type[TCommandHandler]]) -> None:
    """Register commands handlers at injector."""
    injector.get(ICommandBus).register_handlers(handlers)
