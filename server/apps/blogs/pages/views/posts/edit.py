from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from apps.core.logic import queries
from apps.blogs.logic.commands import posts as posts_commands
from apps.blogs.logic.queries import posts as posts_queries
from apps.blogs.models import Post
from apps.core.logic import commands
from apps.core.pages.base_command import BaseCommandView


class _Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "status")


class View(BaseCommandView):
    command = posts_commands.update.Command
    initial_query = posts_queries.retrieve.Query
    template_name = "posts/edit.html"
    form = _Form

    def get_initial_query(self, request: HttpRequest) -> queries.IQuery:
        return self.initial_query(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
            only_owner=True,
        )

    def get_initial_form(
        self,
        request: HttpRequest,
        initial_query_result: posts_queries.retrieve.QueryResult,
    ) -> forms.BaseForm:
        return self.form(instance=initial_query_result.instance)

    def get_command(
        self,
        request: HttpRequest,
        form: _Form,
    ) -> commands.ICommand:
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
        return redirect("blogs:post_detail", command_result.instance.id)
