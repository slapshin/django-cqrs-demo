from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.blogs.logic.commands import posts
from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView


class _Form(forms.Form):
    """Empty form."""


class View(BaseCommandView):
    """Delete post view."""

    command = posts.delete.Command
    form = _Form

    def create_command(
        self,
        request: HttpRequest,
        form: forms.BaseForm | None,
    ) -> commands.ICommand:
        """Create command to execute."""
        return self.command(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: forms.BaseForm | None,
        command_result: posts.delete.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        return redirect("blogs:posts_my")
