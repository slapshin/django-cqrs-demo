import abc
import typing as ty

from pydantic import BaseModel

TQueryResult = ty.TypeVar("TQueryResult")


class IQuery(ty.Generic[TQueryResult], abc.ABC):
    """Query interface."""


class BaseQuery(
    BaseModel,
    IQuery[TQueryResult],
    ty.Generic[TQueryResult],
    metaclass=abc.ABCMeta,
):
    """Base query."""
