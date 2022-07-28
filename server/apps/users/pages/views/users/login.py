from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UsernameField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.core.pages.base_command import BaseCommandView
from apps.users.domain.commands import login


class _Form(forms.Form):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class View(BaseCommandView):
    """Login view."""

    command = login.Command
    template_name = "users/login.html"
    form = _Form

    def create_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> login.Command:
        """Create command to execute."""
        return self.command(
            username=form.data["username"],
            password=form.data["password"],
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: login.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        auth.login(request, command_result.user)
        return redirect("blogs:home")
