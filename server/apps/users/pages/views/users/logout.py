from django import forms
from django.contrib import auth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView
from apps.users.logic.commands import logout


class _Form(forms.Form):
    pass


class View(BaseCommandView):
    command = logout.Command
    form = _Form

    def get_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> commands.ICommand:
        return self.command(
            user_id=self.request.user.id,
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: logout.CommandResult,
    ) -> HttpResponse:
        auth.logout(request)
        return redirect("blogs:home")
