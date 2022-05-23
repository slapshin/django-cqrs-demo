import abc

from pydantic import BaseModel


class IQuery:
    """Query interface."""


class BaseQuery(BaseModel, IQuery, metaclass=abc.ABCMeta):
    """Base query."""
