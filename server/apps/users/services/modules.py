import injector

from apps.users import services
from apps.users.logic import interfaces


class UserInfrastructureServicesModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.IAuthenticationService,
            services.AuthenticationService,
            scope=injector.singleton,
        )
