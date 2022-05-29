from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core.logic.commands.shortcuts import register_commands


class AppConfig(BaseAppConfig):
    """Application "users" config."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """App ready callback."""
        from apps.users.logic.commands import (  # noqa: WPS433
            login,
            logout,
            register,
            send_registration_notification,
        )

        super().ready()

        register_commands(
            (
                register.CommandHandler,
                login.CommandHandler,
                logout.CommandHandler,
                send_registration_notification.CommandHandler,
            ),
        )
