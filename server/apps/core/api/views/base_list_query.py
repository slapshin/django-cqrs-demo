import abc
import typing as ty

from django.core.paginator import InvalidPage
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.core.api.serializers.input.pagination import PaginationMixin
from apps.core.api.views import BaseQueryView
from apps.core.logic.queries.types import Pagination
from apps.users.api.pagination.query import ListPagination


class _PageSerializer(serializers.Serializer):
    count = serializers.IntegerField(allow_null=True)

    def __init__(
        self,
        instances_serializer: ty.Type[serializers.Serializer],
        *args,
        **kwargs,
    ):
        self._instances_serializer = instances_serializer
        super().__init__(*args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()
        fields["results"] = self._instances_serializer(many=True)

        return fields


class BaseListQueryView(BaseQueryView, metaclass=abc.ABCMeta):
    """Base class for list api requests."""

    action = "list"
    pagination = ListPagination

    @classmethod
    def get_swagger_responses(cls):
        """Swagger customization."""
        responses = super().get_swagger_responses()

        responses[cls.success_status] = (
            _PageSerializer(cls.output_serializer)
            if cls.pagination
            else cls.output_serializer(many=True)
        )

        return responses

    def build_response(self, query_result) -> Response:
        """Build response from query result."""
        object_list = self.create_output_dto(query_result)
        if self.pagination:
            return Response(
                {
                    "count": query_result.total,
                    "results": object_list,
                },
            )

        return Response(object_list)

    def create_output_dto(self, query_result) -> dict[str, ty.Any]:
        """Creates output dto based on query result."""
        output_serializer = self.create_output_serializer(
            query_result,
            query_result.instances,
            many=True,
            check_cache=True,
        )

        if isinstance(query_result.instances, models.QuerySet):
            output_serializer.instance = (
                output_serializer.child.setup_root_queryset(
                    output_serializer.instance,
                )
            )

        return output_serializer.data

    def get_pagination(self) -> Pagination:  # noqa: WPS615
        """Provides pagination."""
        if not self.pagination:
            raise ValueError("'pagination' is not defined")

        is_bad_serializer_class = not self.input_serializer or not issubclass(
            self.input_serializer,
            PaginationMixin,
        )

        if is_bad_serializer_class:
            raise ValueError("'input_serializer' should have PaginationMixin")

        input_dto = self.extract_input_dto()

        return Pagination(
            page_size=self.pagination.get_page_size(input_dto),
            page_number=self.pagination.get_page_number(input_dto),
        )

    def handle_exception(self, err):
        """Handle error."""
        if isinstance(err, InvalidPage):
            err = NotFound(_("Invalid page."))

        return super().handle_exception(err)
