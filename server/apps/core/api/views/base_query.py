import abc
import typing as ty
from http import HTTPStatus

from drf_spectacular.types import OpenApiTypes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.core.api.docs import SwaggerSchema
from apps.core.api.views.base_api import BaseAPIView
from apps.core.logic import queries


class BaseQueryView(BaseAPIView, metaclass=abc.ABCMeta):  # noqa: WPS214
    """Base query view."""

    query: ty.ClassVar[ty.Type[queries.IQuery]]
    action: str = ""
    output_serializer: ty.ClassVar[ty.Type[Serializer]]
    input_serializer: ty.ClassVar[ty.Type[Serializer]]
    success_status: HTTPStatus = HTTPStatus.OK

    @classmethod
    def get_swagger_schema(cls) -> SwaggerSchema:
        """Provides swagger schema."""
        kwargs = {}
        if cls.input_serializer:
            kwargs["query_serializer"] = cls.input_serializer

        return SwaggerSchema(
            responses=cls.get_swagger_responses(),
            **kwargs,
        )

    @classmethod
    def get_swagger_responses(cls) -> dict[HTTPStatus, ty.Any]:
        """Provides swagger responses."""
        return {
            cls.success_status: cls.output_serializer,
            HTTPStatus.BAD_REQUEST: OpenApiTypes.NONE,
            HTTPStatus.NOT_FOUND: OpenApiTypes.NONE,
            HTTPStatus.INTERNAL_SERVER_ERROR: OpenApiTypes.NONE,
        }

    def handle_request(self, request: Request, **kwargs) -> Response:
        """Handle request."""
        self._input_dto = None

        return self.build_response(self.execute_query())

    def build_response(self, query_result) -> Response:
        """Build response from query result."""
        return Response(self.create_output_dto(query_result))

    def create_query(self) -> queries.IQuery:
        """Create query to execute."""
        raise NotImplementedError()

    def extract_input_dto(self):
        """Get input dto."""
        if self._input_dto is None:
            if not self.input_serializer:
                raise ValueError("'input_serializer' is not defined")

            serializer = self.input_serializer(data=self.request.query_params)
            serializer.is_valid(raise_exception=True)

            self._input_dto = serializer.validated_data

        return self._input_dto

    def create_output_dto(self, query_result) -> dict[str, ty.Any]:
        """Get output dto."""
        return self.create_output_serializer(query_result).data

    def get_serializer_context(self) -> dict[str, ty.Any]:
        """Get serializer context."""
        context = super().get_serializer_context()
        context["action"] = self.action or None

        return context

    def create_output_serializer(
        self,
        query_result,
        *args,
        **kwargs,
    ) -> Serializer:
        """Create output serializer."""
        if not self.output_serializer:
            raise ValueError("'output_serializer' is not defined")

        kwargs.setdefault(
            "context",
            self.get_output_serializer_context(query_result),
        )
        return self.output_serializer(*args, **kwargs)

    def execute_query(self) -> ty.Any:
        """Execute query."""
        query = self.create_query()
        return queries.execute_query(query)

    def get_output_serializer_context(self, query_result) -> dict[str, ty.Any]:
        """Create output serializer context."""
        return self.get_serializer_context()
