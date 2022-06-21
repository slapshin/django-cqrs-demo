import abc
import typing as ty

from pydantic import BaseModel

from apps.core.logic.messages.interfaces import IMessage, IMessageHandler

TMessageResult = ty.TypeVar("TMessageResult")


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


class BaseQuery(
    BaseMessage[TMessageResult],
    ty.Generic[TMessageResult],
    metaclass=abc.ABCMeta,
):
    """Base class for query."""


class BaseCommand(
    BaseMessage[TMessageResult],
    ty.Generic[TMessageResult],
    metaclass=abc.ABCMeta,
):
    """Base class for command."""


TQuery = ty.TypeVar(
    "TQuery",
    bound=BaseQuery[TMessageResult],  # type: ignore
)

TCommand = ty.TypeVar(
    "TCommand",
    bound=BaseQuery[TMessageResult],  # type: ignore
)


class BaseQueryHandler(
    IMessageHandler[TQuery],
    ty.Generic[TQuery],
    metaclass=abc.ABCMeta,
):
    """Base class for query handler."""


class BaseCommandHandler(
    IMessageHandler[TCommand],
    ty.Generic[TCommand],
    metaclass=abc.ABCMeta,
):
    """Base class for command handler."""
