import typing as ty

from django.db import models

from apps.core.pages.base_query import BaseQueryView


@ty.runtime_checkable
class InstancesQueryResult(ty.Protocol):
    """Query result with instances queryset field."""

    instances: models.QuerySet


class BaseListQueryView(BaseQueryView):
    """Base list query view."""

    def get_context_data(self, **kwargs):
        """Provides context data."""
        query_result = self.execute_query(self.request)
        context = super().get_context_data(**kwargs)

        if isinstance(query_result, InstancesQueryResult):
            context["instances"] = query_result.instances

        return context
