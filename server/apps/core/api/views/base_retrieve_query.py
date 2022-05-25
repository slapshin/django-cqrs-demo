import abc

from rest_framework.exceptions import NotFound

from apps.core.api.views import BaseQueryView
from apps.core.logic.queries.types import RetrieveQueryResult


class BaseRetrieveQueryView(BaseQueryView, metaclass=abc.ABCMeta):
    """Base retrieve query view."""

    def create_output_dto(self, query_result):
        """Extract output dto from query result."""
        if not isinstance(query_result, RetrieveQueryResult):
            raise ValueError('Query result must have "instance" field')

        if not query_result.instance:
            raise NotFound()

        output_serializer = self.create_output_serializer(
            query_result,
            query_result.instance,
        )

        return output_serializer.data
