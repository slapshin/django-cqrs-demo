import abc
import typing as ty

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


TMessage = ty.TypeVar(
    "TMessage",
    bound=IMessage[TMessageResult],  # type: ignore
)


class IMessageHandler(
    ty.Generic[TMessage],
    metaclass=abc.ABCMeta,
):
    """Base message handler."""

    @abc.abstractmethod
    def execute(self, message: TMessage) -> TMessageResult:
        """Main logic here."""


TCommandHandler = ty.TypeVar(
    "TCommandHandler",
    bound=IMessageHandler[TMessage],  # type: ignore
)


class IMessagesBus(abc.ABC):
    """Messages dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        message_handler: ty.Type[TCommandHandler],
    ) -> None:
        """Register message handler."""

    @abc.abstractmethod
    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[TCommandHandler]],
    ) -> None:
        """Register batch messages handlers."""

    @abc.abstractmethod
    def dispatch(self, message: IMessage[TMessageResult]) -> TMessageResult:
        """Send command and get result."""

    @abc.abstractmethod
    def dispatch_async(self, message: IMessage[TMessageResult]) -> None:
        """Send command for async execution."""
