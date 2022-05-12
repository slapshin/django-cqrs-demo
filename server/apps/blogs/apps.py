from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core.logic.commands.facades import register_commands
from apps.core.logic.queries.facades import register_queries


class AppConfig(BaseAppConfig):
    """Application "blogs" config."""

    name = "apps.blogs"
    verbose_name = _("VN__BLOGS")

    def ready(self):
        """App ready callback."""
        from apps.blogs.logic.commands.main import COMMANDS  # noqa: WPS433
        from apps.blogs.logic.queries.main import QUERIES  # noqa: WPS433

        super().ready()

        register_queries(QUERIES)
        register_commands(COMMANDS)
