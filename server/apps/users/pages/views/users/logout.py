from django import forms
from django.contrib import auth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView
from apps.users.logic.commands import logout


class _Form(forms.Form):
    """Empty form."""


class View(BaseCommandView):
    """Logout view."""

    command = logout.Command
    form = _Form

    def create_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> commands.ICommand:
        """Create command to execute."""
        return self.command(
            user_id=request.user.id if request.user.is_authenticated else None,
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: logout.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        auth.logout(request)
        return redirect("blogs:home")

    def handle_command_fail(
        self,
        request: HttpRequest,
        form: forms.BaseForm,
    ) -> HttpResponse:
        """Handle failed command execution."""
        return redirect("blogs:home")
