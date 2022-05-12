import abc
import typing as ty

from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandHandler
from apps.core.logic.commands.handler import TResult

CommandInfo = ty.Tuple[
    ty.Type[ICommand],
    ty.Type[ICommandHandler[ICommand, TResult]],
]


class ICommandBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register(
        self,
        command_type: ty.Type[ICommand],
        command_handler: ty.Type[ICommandHandler[ICommand, TResult]],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def register_many(self, handlers: list[CommandInfo]) -> None:
        """Register many command handlers."""

    @abc.abstractmethod
    def dispatch(self, command: ICommand) -> TResult:
        """Send command and get result."""


class CommandBus(ICommandBus):
    """Queries dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register(
        self,
        command_type: ty.Type[ICommand],
        command_handler: ty.Type[ICommandHandler[ICommand, TResult]],
    ) -> None:
        """Register command handler."""
        self._registry[command_type] = command_handler

    def register_many(self, handlers: list[CommandInfo]) -> None:
        """Register many command handlers."""
        for command, command_handler in handlers:
            self.register(command, command_handler)

    def dispatch(self, command: ICommand) -> TResult:
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(command))
        if not handler_type:
            raise ValueError(
                'Handler for command "{0}" is not registered'.format(
                    type(command),
                ),
            )
        command_handler = injector.get(handler_type)
        return command_handler.execute(command)
