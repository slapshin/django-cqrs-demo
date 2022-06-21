import typing as ty

from django.db import transaction

from apps.core import injector
from apps.core.logic.messages.interfaces import (
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
