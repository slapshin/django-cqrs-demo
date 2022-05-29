import abc
import typing as ty

from pydantic import BaseModel

TCommandResult = ty.TypeVar("TCommandResult")


class ICommand(ty.Generic[TCommandResult], abc.ABC):
    """Command interface."""

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, string_data: str) -> "ICommand[TCommandResult]":
        """Deserialize object."""

    @abc.abstractmethod
    def serialize(self) -> str:
        """Serialize object."""


class BaseCommand(
    BaseModel,
    ICommand[TCommandResult],
    ty.Generic[TCommandResult],
    metaclass=abc.ABCMeta,
):
    """Base command based pydantic."""

    @classmethod
    def deserialize(cls, string_data: str) -> ICommand[TCommandResult]:
        """Deserialize object."""
        return cls.parse_raw(string_data)

    def serialize(self) -> str:
        """Serialize object."""
        return self.json()
