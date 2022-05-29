import abc
import typing as ty

from apps.core.logic.commands import ICommand, TCommandResult

TCommand = ty.TypeVar("TCommand", bound=ICommand[TCommandResult])


class ICommandHandler(
    ty.Generic[TCommand],
    metaclass=abc.ABCMeta,
):
    """Base command handler."""

    @abc.abstractmethod
    def execute(self, command: TCommand) -> TCommandResult:
        """Main logic here."""


TCommandHandler = ty.TypeVar(
    "TCommandHandler",
    bound=ICommandHandler[ICommand[TCommandResult]],
)
