from django.contrib import auth
from rest_framework.response import Response

from apps.core.api.views import BaseCommandView
from apps.users.domain.commands import logout


class View(BaseCommandView):
    """Logout view."""

    command = logout.Command

    def create_command(self) -> logout.Command:
        """Create command to execute."""
        return self.command(
            user_id=self.user.id if self.user else None,
        )

    def build_response(self, command_result: logout.CommandResult) -> Response:
        """Build response from command result."""
        auth.logout(self.request)
        return super().build_response(command_result)
