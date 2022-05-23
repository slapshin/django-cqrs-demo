import typing as ty

from apps.core import injector
from apps.core.helpers.module_loading import import_string
from apps.core.logic.commands import ICommand, ICommandBus
from celery_app import app


@app.task
def execute_command_async_task(command_class: str, command_data: str):
    """Deserialize and execute command."""
    command_cls: ty.Type[ICommand] = import_string(command_class)
    command = command_cls.deserialize(command_data)

    command_bus = injector.get(ICommandBus)
    return command_bus.dispatch(command)
