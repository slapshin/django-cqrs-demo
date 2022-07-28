import typing as ty

from apps.core import injector
from apps.core.domain.messages.interfaces import (
    IMessage,
    IMessageHandler,
    IMessagesBus,
    TMessageResult,
)


def dispatch_message(message: IMessage[TMessageResult]) -> TMessageResult:
    """Dispatch message."""
    messages_bus = injector.get(IMessagesBus)
    return messages_bus.dispatch(message)


def dispatch_message_async(message: IMessage[TMessageResult]) -> None:
    """Dispatch message async."""
    messages_bus = injector.get(IMessagesBus)
    messages_bus.dispatch_async(message)


def register_messages_handlers(*args: ty.Type[IMessageHandler]) -> None:
    """Register messages handlers at injector."""
    injector.get(IMessagesBus).register_handlers(args)
