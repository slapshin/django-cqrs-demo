import injector

from apps.core import services
from apps.core.logic import interfaces


class CodeInfrastructureModule(injector.Module):
    """Setup di for core infrastructure services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.IEMailService,
            services.EMailService,
            scope=injector.singleton,
        )
