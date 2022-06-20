import typing as ty

from django.http import HttpRequest
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from apps.core.logic import bus, messages
from apps.core.pages.base import BaseView


class BaseQueryView(TemplateResponseMixin, ContextMixin, BaseView):
    """Base query view."""

    query: ty.Type[messages.IMessage]

    def get(self, request, *args, **kwargs):
        """Handle GET request."""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def execute_query(self, request: HttpRequest):
        """Execute query."""
        query = self.create_query(request)
        return bus.dispatch_message(query)

    def create_query(self, request: HttpRequest) -> messages.IMessage:
        """Create query to execute."""
        raise NotImplementedError()
