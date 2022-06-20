import abc
import typing as ty

from pydantic import BaseModel

TMessageResult = ty.TypeVar("TMessageResult")


class IMessage(ty.Generic[TMessageResult], abc.ABC):
    """Command interface."""

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, string_data: str) -> "IMessage[TMessageResult]":
        """Deserialize object."""

    @abc.abstractmethod
    def serialize(self) -> str:
        """Serialize object."""


class BaseMessage(
    BaseModel,
    IMessage[TMessageResult],
    ty.Generic[TMessageResult],
    metaclass=abc.ABCMeta,
):
    """Base pydantic based message."""

    @classmethod
    def deserialize(cls, string_data: str) -> IMessage[TMessageResult]:
        """Deserialize object."""
        return cls.parse_raw(string_data)

    def serialize(self) -> str:
        """Serialize object."""
        return self.json()


TMesssage = ty.TypeVar(
    "TMesssage",
    bound=IMessage[TMessageResult],  # type: ignore
)


class IMessageHandler(
    ty.Generic[TMesssage],
    metaclass=abc.ABCMeta,
):
    """Base message handler."""

    @abc.abstractmethod
    def execute(self, message: TMesssage) -> TMessageResult:
        """Main logic here."""
