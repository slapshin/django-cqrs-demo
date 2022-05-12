import typing as ty

from django.forms import forms
from django.http import HttpResponse, HttpRequest
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from apps.core.errors import BaseError
from apps.core.logic import commands, queries
from apps.core.pages.base import BaseView


class BaseCommandView(TemplateResponseMixin, ContextMixin, BaseView):
    """Base command view."""

    command: ty.Type[commands.ICommand]
    initial_query: ty.Type[queries.IQuery] | None = None
    form: ty.Type[forms.BaseForm] | None = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.template_name:
            return self.http_method_not_allowed(request, *args, **kwargs)

        query_result = None
        if self.initial_query:
            query = self.get_initial_query(request)
            query_result = queries.execute_query(query)

        return self.render_to_response(
            context=self.get_context_data(
                form=self.get_initial_form(request, query_result),
                **kwargs,
            ),
        )

    def get_initial_query(self, request: HttpRequest) -> queries.IQuery:
        raise NotImplementedError()

    def get_initial_form(
            self,
            request: HttpRequest,
            initial_query_result,
    ) -> forms.BaseForm:
        return self.form()

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            command = self.get_command(request, form)

            try:
                command_result = commands.execute_command(command)
            except (BaseError, ValueError) as err:
                form.add_error(None, str(err))
            else:
                return self.handle_command_success(
                    request=request,
                    form=form,
                    command_result=command_result,
                )

        return self.handle_command_fail(
            request=request,
            form=form,
        )

    def handle_command_success(
            self,
            request: HttpRequest,
            form: forms.BaseForm,
            command_result,
    ) -> HttpResponse:
        return self.render_to_response(
            context=self.get_context_data(form=form),
        )

    def handle_command_fail(
            self,
            request: HttpRequest,
            form: forms.BaseForm,
    ) -> HttpResponse:
        return self.render_to_response(
            context=self.get_context_data(form=form),
        )

    def get_command(
            self,
            request: HttpRequest,
            form: forms.BaseForm,
    ) -> commands.ICommand:
        raise NotImplementedError()
