import typing as ty
from dataclasses import dataclass

from django.db import models


@dataclass
class Pagination:
    """Pagination fields."""

    page_size: int | None = None
    page_number: int | None = 1


@ty.runtime_checkable
class RetrieveQueryResult(ty.Protocol):
    """Query result with instance field."""

    instance: models.Model


@ty.runtime_checkable
class ListQueryResult(ty.Protocol):
    """Query result with instances queryset field."""

    instances: models.QuerySet
