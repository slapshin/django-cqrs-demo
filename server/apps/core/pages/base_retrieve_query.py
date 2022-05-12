import typing as ty

from django.db import models

from apps.core.pages.base_query import BaseQueryView


@ty.runtime_checkable
class InstanceQueryResult(ty.Protocol):
    """Query result with instances queryset field."""

    instance: models.Model


class BaseRetrieveQueryView(BaseQueryView):
    """Base retrieve query view."""

    def get_context_data(self, **kwargs):
        query_result = self.execute_query(self.request)
        context = super().get_context_data(**kwargs)

        if isinstance(query_result, InstanceQueryResult):
            context["instance"] = query_result.instance

        return context
