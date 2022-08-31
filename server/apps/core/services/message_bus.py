import typing as ty

from django.db import transaction
from pydantic import BaseModel

from apps.core import injector
from apps.core.logic.messages.interfaces import (
    IMessage,
    IMessageHandler,
    IMessagesBus,
    TCommandHandler,
    TMessageResult,
)
from apps.core.tasks.messages import execute_message_async_task


class MessagesBus(IMessagesBus):
    """Messages dispatcher."""

    def __init__(self) -> None:
        """Initializing."""
        self._registry: dict[ty.Type[IMessage], ty.Type[TCommandHandler]] = {}

    def register_handler(
        self,
        message_handler: ty.Type[TCommandHandler],
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
        handlers: ty.Iterable[ty.Type[TCommandHandler]],
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
        return message_handler.handle(message)

    def dispatch_async(self, message: IMessage[TMessageResult]) -> None:
        """Send command for async execution."""
        serialized_message = self._serialize_message(message)
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

    def _serialize_message(self, message: IMessage[TMessageResult]) -> str:
        if isinstance(message, BaseModel):
            return message.json()

        raise ValueError("Can't serialize message: {0}".format(message))
