from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core.logic.commands.facades import register_commands


class AppConfig(BaseAppConfig):
    """Application "users" config."""

    name = "apps.users"
    verbose_name = _("VN__USERS")

    def ready(self):
        """App ready callback."""
        from apps.users.logic.commands.main import COMMANDS  # noqa: WPS433

        super().ready()

        register_commands(COMMANDS)
