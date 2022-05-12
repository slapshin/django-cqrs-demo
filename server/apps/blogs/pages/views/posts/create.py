from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.blogs.logic.commands import posts
from apps.blogs.models import Post
from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView


class _Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "status")


class View(BaseCommandView):
    """Post create view."""

    command = posts.create.Command
    template_name = "posts/create.html"
    form = _Form

    def create_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> commands.ICommand:
        """Create command to execute."""
        return self.command(
            user_id=request.user.id if request.user.is_authenticated else None,
            title=form.data["title"],
            content=form.data["content"],
            status=form.data["status"],
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: posts.create.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        return redirect("blogs:post_detail", command_result.instance.id)
