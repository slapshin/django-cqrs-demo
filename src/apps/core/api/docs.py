import typing as ty
from dataclasses import dataclass

from drf_spectacular.generators import SchemaGenerator as BaseSchemaGenerator
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

SwaggerSchemaResponse = ty.Union[
    int,
    str,
    OpenApiTypes,
    serializers.Serializer,
    None,
]


@dataclass(frozen=True)
class SwaggerSchema:
    """Swagger schema."""

    responses: dict[int, SwaggerSchemaResponse | None]
    request_body: ty.Any | None = None
    query_serializer: ty.Any | None = None
    operation_description: str | None = None
    operation_summary: str | None = None


class SchemaGenerator(BaseSchemaGenerator):
    """Schema generator."""
