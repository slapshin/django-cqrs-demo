import injector

from apps.users.logic import interfaces, services


class UserLogicServicesModule(injector.Module):
    """Setup di for user application services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.ISignupService,
            services.SignupService,
            scope=injector.singleton,
        )
