import abc
import typing as ty

from rest_framework.response import Response

from apps.core.api.views import BaseQueryView
from apps.core.logic.messages.types import ListQueryResult


class BaseListQueryView(BaseQueryView, metaclass=abc.ABCMeta):
    """Base class for list api requests."""

    @classmethod
    def get_swagger_responses(cls):
        """Swagger customization."""
        responses = super().get_swagger_responses()
        responses[cls.success_status] = cls.output_serializer(many=True)

        return responses

    def build_response(self, query_result) -> Response:
        """Build response from query result."""
        object_list = self.create_output_dto(query_result)

        return Response(object_list)

    def create_output_dto(self, query_result) -> dict[str, ty.Any]:
        """Creates output dto based on query result."""
        if not isinstance(query_result, ListQueryResult):
            raise ValueError('Query result must have "instances" field')

        output_serializer = self.create_output_serializer(
            query_result,
            query_result.instances,
            many=True,
        )

        return output_serializer.data
