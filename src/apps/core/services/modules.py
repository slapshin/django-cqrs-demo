import injector

from apps.core import services
from apps.core.logic import interfaces
from apps.core.logic.messages.interfaces import IMessagesBus


class CodeInfrastructureModule(injector.Module):
    """Setup di for core infrastructure services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            IMessagesBus,
            services.MessagesBus,
            scope=injector.singleton,
        )
        binder.bind(
            interfaces.IEMailService,
            services.EMailService,
            scope=injector.singleton,
        )
