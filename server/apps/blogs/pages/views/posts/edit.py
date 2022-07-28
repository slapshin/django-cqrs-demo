from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.blogs.domain.commands import posts as posts_commands
from apps.blogs.domain.queries import posts as posts_queries
from apps.blogs.models import Post
from apps.core.pages.base_command import BaseCommandView


class _Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "status")


class View(BaseCommandView):
    """Post edit view."""

    command = posts_commands.update.Command
    initial_query = posts_queries.retrieve.Query
    template_name = "posts/edit.html"
    form = _Form

    def create_initial_query(
        self,
        request: HttpRequest,
    ) -> posts_queries.retrieve.Query:
        """Provides initial query for command view."""
        return self.initial_query(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
            only_owner=True,
        )

    def create_initial_form(
        self,
        request: HttpRequest,
        initial_query_result: posts_queries.retrieve.QueryResult,
    ) -> forms.BaseForm:
        """Provides initial form for command view."""
        return self.form(instance=initial_query_result.instance)

    def create_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> posts_commands.update.Command:
        """Create command to execute."""
        return self.command(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
            title=form.data["title"],
            content=form.data["content"],
            status=form.data["status"],
        )

    def handle_command_success(
        self,
        request: HttpRequest,
        form: _Form,
        command_result: posts_commands.create.CommandResult,
    ) -> HttpResponse:
        """Handle success command execution."""
        return redirect("blogs:post_detail", command_result.instance.id)
