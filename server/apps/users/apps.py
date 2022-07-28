from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core import injector
from apps.core.services.messages import register_messages_handlers


class AppConfig(BaseAppConfig):
    """Application "users" config."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """App ready callback."""
        from apps.users.domain.commands import (  # noqa: WPS433
            login,
            logout,
            register,
            send_registration_notification,
        )
        from apps.users.services.modules import (  # noqa: WPS433
            UserInfrastructureServicesModule,
        )

        super().ready()

        injector.binder.install(UserInfrastructureServicesModule)

        register_messages_handlers(
            # commands
            register.CommandHandler,
            login.CommandHandler,
            logout.CommandHandler,
            send_registration_notification.CommandHandler,
        )
