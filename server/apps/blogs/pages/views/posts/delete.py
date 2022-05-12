from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.logic import queries
from apps.blogs.logic.commands import posts
from apps.blogs.logic.queries import posts as posts_queries
from apps.blogs.models import Post
from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView


class _Form(forms.Form):
    """Empty form."""


class View(BaseCommandView):
    command = posts.delete.Command
    form = _Form

    def get_command(
            self,
            request: HttpRequest,
            form: forms.BaseForm | None,
    ) -> commands.ICommand:
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
        return redirect("blogs:posts_my")
