from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView
from apps.users.logic.commands import register
from apps.users.models import User


class _Form(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class View(BaseCommandView):
    command = register.Command
    template_name = "users/register.html"
    form = _Form

    def get_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> commands.ICommand:
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
        messages.success(request, "Registration successful.")
        auth.login(request, command_result.user)
        return redirect("blogs:home")
