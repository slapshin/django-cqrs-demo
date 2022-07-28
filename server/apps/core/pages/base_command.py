import typing as ty

from django.forms import forms
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from apps.core.domain import messages
from apps.core.domain.errors import AccessDeniedDomainError
from apps.core.errors import BaseError
from apps.core.pages.base import BaseView
from apps.core.services.messages import dispatch_message


class BaseCommandView(TemplateResponseMixin, ContextMixin, BaseView):
    """Base command view."""

    command: ty.Type[messages.BaseCommand]
    initial_query: ty.Type[messages.BaseQuery] | None = None
    form: ty.Type[forms.BaseForm]

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle GET request."""
        if not self.template_name:
            return self.http_method_not_allowed(request, *args, **kwargs)

        query_result = None
        if self.initial_query:
            query = self.create_initial_query(request)
            query_result = dispatch_message(query)

        return self.render_to_response(
            context=self.get_context_data(
                form=self.create_initial_form(request, query_result),
                **kwargs,
            ),
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle POST request."""
        form = self.form(request.POST)
        if form.is_valid():
            command = self.create_command(request, form)

            try:
                command_result = dispatch_message(command)
            except AccessDeniedDomainError:  # noqa: WPS329
                raise
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

    def create_initial_query(self, request: HttpRequest) -> messages.BaseQuery:
        """Provides initial query for command view."""
        raise NotImplementedError()

    def create_initial_form(
        self,
        request: HttpRequest,
        initial_query_result,
    ) -> forms.BaseForm:
        """Provides initial form for command view."""
        return self.form()

    def handle_command_success(
        self,
        request: HttpRequest,
        form: forms.BaseForm,
        command_result,
    ) -> HttpResponse:
        """Handle success command execution."""
        return self.render_to_response(
            context=self.get_context_data(form=form),
        )

    def handle_command_fail(
        self,
        request: HttpRequest,
        form: forms.BaseForm,
    ) -> HttpResponse:
        """Handle failed command execution."""
        return self.render_to_response(
            context=self.get_context_data(form=form),
        )

    def create_command(
        self,
        request: HttpRequest,
        form: forms.BaseForm,
    ) -> messages.BaseCommand:
        """Create command to execute."""
        raise NotImplementedError()
