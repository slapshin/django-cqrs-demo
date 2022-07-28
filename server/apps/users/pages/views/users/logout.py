from django import forms
from django.contrib import auth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.domain.errors import AccessDeniedDomainError
from apps.core.errors import BaseError
from apps.core.pages.base_command import BaseCommandView
from apps.users.domain.commands import logout


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
    ) -> logout.Command:
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

    def handle_error(
        self,
        request: HttpRequest,
        err: BaseError,
    ) -> HttpResponse:
        """Process errors."""
        if isinstance(err, AccessDeniedDomainError):
            return redirect("blogs:home")

        return super().handle_error(request, err)
