import injector

from apps.core.logic import bus


class CoreApplicationModule(injector.Module):
    """Setup di for core applications services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            bus.IMessagesBus,
            bus.MessagesBus,
            scope=injector.singleton,
        )
