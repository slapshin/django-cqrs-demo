import injector

from apps.core.logic.commands import bus as command_bus
from apps.core.logic.queries import bus as query_bus


class CoreApplicationModule(injector.Module):
    """Setup di for core applications services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            command_bus.ICommandBus,
            command_bus.CommandBus,
            scope=injector.singleton,
        )
        binder.bind(
            query_bus.IQueryBus,
            query_bus.QueryBus,
            scope=injector.singleton,
        )
