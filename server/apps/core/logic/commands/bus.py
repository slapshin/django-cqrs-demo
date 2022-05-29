import abc
import typing as ty

from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandHandler
from apps.core.logic.commands.handler import TCommandHandler, TCommandResult


class ICommandBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        command_handler: ty.Type[TCommandHandler],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[TCommandHandler]],
    ) -> None:
        """Register many command handlers."""

    @abc.abstractmethod
    def dispatch(self, command: ICommand[TCommandResult]) -> TCommandResult:
        """Send command and get result."""


class CommandBus(ICommandBus):
    """Queries dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        command_handler: ty.Type[TCommandHandler],
    ) -> None:
        """Register command handler."""
        command_type: ICommand[TCommandResult] | None = None
        for orig_base in command_handler.__orig_bases__:
            origin = ty.get_origin(orig_base)
            if origin and issubclass(origin, ICommandHandler):
                command_type = ty.get_args(orig_base)[0]

        if not command_type:
            raise ValueError(
                'Can\'t extract command from handler "{0}"'.format(
                    command_handler,
                ),
            )

        self._registry[command_type] = command_handler

    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[TCommandHandler]],
    ) -> None:
        """Register many command handlers."""
        for command_handler in handlers:
            self.register_handler(command_handler)

    def dispatch(self, command: ICommand[TCommandResult]) -> TCommandResult:
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
