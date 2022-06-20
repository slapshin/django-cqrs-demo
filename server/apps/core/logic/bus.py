import abc
import typing as ty

from django.db import transaction

from apps.core import injector
from apps.core.logic.messages import IMessage, IMessageHandler, TMessageResult


class IMessagesBus(abc.ABC):
    """Messages dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        message_handler: ty.Type[IMessageHandler],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[IMessageHandler]],
    ) -> None:
        """Register many command handlers."""

    @abc.abstractmethod
    def dispatch(self, command: IMessage[TMessageResult]) -> TMessageResult:
        """Send command and get result."""


class MessagesBus(IMessagesBus):
    """Messages dispatcher."""

    def __init__(self) -> None:
        """Initializing."""
        self._registry: dict[ty.Type[IMessage], ty.Type[IMessageHandler]] = {}

    def register_handler(
        self,
        message_handler: ty.Type[IMessageHandler],
    ) -> None:
        """Register message handler."""
        message_type: ty.Type[IMessage[TMessageResult]] | None = None
        for orig_base in message_handler.__orig_bases__:
            origin = ty.get_origin(orig_base)
            if origin and issubclass(origin, IMessageHandler):
                message_type = ty.get_args(orig_base)[0]

        if not message_type:
            raise ValueError(
                'Can\'t extract message type from handler "{0}"'.format(
                    message_handler,
                ),
            )

        self._registry[message_type] = message_handler

    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[IMessageHandler]],
    ) -> None:
        """Register many messages handlers."""
        for command_handler in handlers:
            self.register_handler(command_handler)

    def dispatch(self, message: IMessage[TMessageResult]) -> TMessageResult:
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(message))
        if not handler_type:
            raise ValueError(
                'Handler for message "{0}" is not registered'.format(
                    type(message),
                ),
            )
        message_handler = injector.get(handler_type)
        return message_handler.execute(message)


def dispatch_message(message: IMessage[TMessageResult]) -> TMessageResult:
    """Dispatch message."""
    messages_bus = injector.get(IMessagesBus)
    return messages_bus.dispatch(message)


def dispatch_message_async(message: IMessage[TMessageResult]) -> None:
    """Dispatch message async."""
    from apps.core.tasks.messages import (  # noqa: WPS433
        execute_message_async_task,
    )

    serialized_message = message.serialize()
    message_type = type(message)

    transaction.on_commit(
        lambda: execute_message_async_task.delay(
            message_class="{0}.{1}".format(
                message_type.__module__,
                message_type.__name__,
            ),
            message_data=serialized_message,
        ),
    )


def register_messages_handlers(*args: ty.Type[IMessageHandler]) -> None:
    """Register messages handlers at injector."""
    injector.get(IMessagesBus).register_handlers(args)
