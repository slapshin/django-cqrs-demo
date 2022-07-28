import typing as ty

from django.db import models


@ty.runtime_checkable
class RetrieveQueryResult(ty.Protocol):
    """Query result with instance field."""

    instance: models.Model


@ty.runtime_checkable
class ListQueryResult(ty.Protocol):
    """Query result with instances queryset field."""

    instances: models.QuerySet
