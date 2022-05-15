import abc

from rest_framework.exceptions import NotFound

from apps.core.api.views import BaseQueryView


class BaseRetrieveQueryView(BaseQueryView, metaclass=abc.ABCMeta):
    """Base retrieve query view."""

    action = "retrieve"

    def get_instance(self, query_result):
        """Get instance."""
        instance = query_result.instance
        if not instance:
            raise NotFound()

        return instance

    def create_output_dto(self, query_result):
        """Extract output dto from query result."""
        output_serializer = self.create_output_serializer(
            query_result,
            query_result.instance,
        )

        return output_serializer.data
