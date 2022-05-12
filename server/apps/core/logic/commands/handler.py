import abc
import typing as ty

TCommand = ty.TypeVar("TCommand")
TResult = ty.TypeVar("TResult")


class ICommandHandler(ty.Generic[TCommand, TResult], metaclass=abc.ABCMeta):
    """Base command handler."""

    @abc.abstractmethod
    def execute(self, command: TCommand) -> TResult:
        """Main logic here."""
