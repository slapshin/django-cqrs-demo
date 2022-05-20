import abc
import typing as ty
from http import HTTPStatus

from drf_spectacular.types import OpenApiTypes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.core.api.docs import SwaggerSchema
from apps.core.api.views.base_api import BaseAPIView
from apps.core.logic import commands


class BaseCommandView(BaseAPIView, metaclass=abc.ABCMeta):  # noqa: WPS214
    """Base command view."""

    command: ty.ClassVar[ty.Type[commands.ICommand]]
    output_serializer: ty.ClassVar[ty.Type[Serializer] | None] = None
    input_serializer: ty.ClassVar[ty.Type[Serializer]]
    success_status: HTTPStatus = HTTPStatus.OK

    @classmethod
    def get_swagger_schema(cls) -> SwaggerSchema:
        """Returns swagger schema."""
        kwargs = {}
        if cls.input_serializer:
            kwargs["request_body"] = cls.input_serializer

        return SwaggerSchema(
            responses=cls.get_swagger_responses(),
            **kwargs,
        )

    @classmethod
    def get_swagger_responses(cls) -> dict[HTTPStatus, ty.Any]:
        """Returns swagger responses."""
        return {
            HTTPStatus.BAD_REQUEST: OpenApiTypes.NONE,
            HTTPStatus.INTERNAL_SERVER_ERROR: OpenApiTypes.NONE,
            cls.success_status: cls.output_serializer or OpenApiTypes.NONE,
        }

    def handle_request(self, request: Request, **kwargs):
        """Process request."""
        command = self.create_command()
        command_result = commands.execute_command(command)

        return self.build_response(command_result)

    def build_response(self, command_result) -> Response:
        """Build response from command result."""
        response_data = (
            self.create_output_dto(command_result)
            if self.output_serializer
            else None
        )

        return Response(
            data=response_data,
            status=self.success_status,
        )

    def create_command(self) -> commands.ICommand:
        """Create command to execute."""
        raise NotImplementedError()

    def extract_input_dto(self):
        """Extracts input data."""
        if not self.input_serializer:
            raise ValueError("'input_serializer' is not defined")

        serializer = self.input_serializer(
            data=self.request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def create_output_dto(self, command_result) -> dict[str, ty.Any]:
        """Build output dto from command result."""
        if not self.output_serializer:
            raise ValueError("'output_serializer' is not defined")

        return self.output_serializer(
            self.get_output_serializer_instance(command_result),
            context=self.get_serializer_context(),
        ).data

    def get_output_serializer_instance(self, command_result) -> ty.Any:
        """Get output serializer instance."""
        return command_result
