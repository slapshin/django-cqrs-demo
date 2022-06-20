import typing as ty

from apps.core.helpers.module_loading import import_string
from apps.core.logic.bus import dispatch_message
from apps.core.logic.messages import IMessage
from celery_app import app


@app.task
def execute_message_async_task(message_class: str, message_data: str) -> None:
    """Deserialize and dispatch message."""
    message_cls: ty.Type[IMessage] = import_string(message_class)
    message = message_cls.deserialize(message_data)

    dispatch_message(message)
