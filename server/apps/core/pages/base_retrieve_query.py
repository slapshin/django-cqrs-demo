from apps.core.logic.types import RetrieveQueryResult
from apps.core.pages.base_query import BaseQueryView


class BaseRetrieveQueryView(BaseQueryView):
    """Base retrieve query view."""

    def get_context_data(self, **kwargs):
        """Provides context data."""
        query_result = self.execute_query(self.request)
        context = super().get_context_data(**kwargs)

        if not isinstance(query_result, RetrieveQueryResult):
            raise ValueError('Query result must have "instance" field')

        context["instance"] = query_result.instance

        return context
