import typing as ty

from pydantic import BaseModel

from apps.core.helpers.module_loading import import_string
from apps.core.logic.messages import dispatch_message
from apps.core.logic.messages.interfaces import IMessage
from celery_app import app


@app.task
def execute_message_async_task(message_class: str, message_data: str) -> None:
    """Deserialize and dispatch message."""
    message_cls: ty.Type[IMessage] = import_string(message_class)

    if not issubclass(message_cls, BaseModel):
        raise ValueError("Can't deserialize message: {0}".format(message_cls))

    message = ty.cast(IMessage, message_cls.parse_raw(message_data))

    dispatch_message(message)
