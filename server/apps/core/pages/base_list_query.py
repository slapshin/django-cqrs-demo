from apps.core.logic.messages.types import ListQueryResult
from apps.core.pages.base_query import BaseQueryView


class BaseListQueryView(BaseQueryView):
    """Base list query view."""

    def get_context_data(self, **kwargs):
        """Provides context data."""
        query_result = self.execute_query(self.request)
        context = super().get_context_data(**kwargs)

        if not isinstance(query_result, ListQueryResult):
            raise ValueError('Query result must have "instances" field')

        context["instances"] = query_result.instances

        return context
