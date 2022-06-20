from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core.logic.bus import register_messages_handlers


class AppConfig(BaseAppConfig):
    """Application "blogs" config."""

    name = "apps.blogs"
    verbose_name = _("VN__BLOGS")

    def ready(self):
        """App ready callback."""
        from apps.blogs.logic.commands import (  # noqa: WPS433
            posts as posts_commands,
        )
        from apps.blogs.logic.queries import (  # noqa: WPS433
            posts as posts_queries,
        )

        super().ready()

        register_messages_handlers(
            # commands
            posts_commands.create.CommandHandler,
            posts_commands.update.CommandHandler,
            posts_commands.delete.CommandHandler,
            # queries
            posts_queries.list.QueryHandler,
            posts_queries.retrieve.QueryHandler,
            posts_queries.my.QueryHandler,
        )
