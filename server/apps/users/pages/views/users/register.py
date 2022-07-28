from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.pages.base_command import BaseCommandView
from apps.users.domain.commands import register
from apps.users.models import User


class _Form(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class View(BaseCommandView):
    """Register view."""

    command = register.Command
    template_name = "users/register.html"
    form = _Form

    def create_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> register.Command:
        """Create command to execute."""
        return self.command(
            email=form.data["email"],
            password1=form.data["password1"],
            password2=form.data["password2"],
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: register.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        auth.login(request, command_result.user)
        return redirect("blogs:home")
