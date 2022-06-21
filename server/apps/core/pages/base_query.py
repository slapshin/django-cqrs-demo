import typing as ty

from django.http import HttpRequest
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from apps.core.logic import messages
from apps.core.pages.base import BaseView


class BaseQueryView(TemplateResponseMixin, ContextMixin, BaseView):
    """Base query view."""

    query: ty.Type[messages.BaseQuery]

    def get(self, request, *args, **kwargs):
        """Handle GET request."""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def execute_query(self, request: HttpRequest):
        """Execute query."""
        query = self.create_query(request)
        return messages.dispatch_message(query)

    def create_query(self, request: HttpRequest) -> messages.BaseQuery:
        """Create query to execute."""
        raise NotImplementedError()
