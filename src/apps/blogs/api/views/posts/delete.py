from http import HTTPStatus

from apps.blogs.logic.commands import posts
from apps.core.api.views import BaseCommandView


class View(BaseCommandView):
    """Post delete view."""

    command = posts.delete.Command
    success_status = HTTPStatus.NO_CONTENT

    def create_command(self) -> posts.delete.Command:
        """Create command to execute."""
        return self.command(
            user_id=self.user.id if self.user else None,
            post_id=self.kwargs["pk"],
        )
