from django.http import HttpRequest
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from apps.core.logic import queries
from apps.core.pages.base import BaseView

import typing as ty


class BaseQueryView(TemplateResponseMixin, ContextMixin, BaseView):
    """Base query view."""
    query: ty.Type[queries.IQuery]

    def execute_query(self, request: HttpRequest):
        query = self.get_query(request)
        return queries.execute_query(query)

    def get_query(self, request: HttpRequest) -> queries.IQuery:
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
