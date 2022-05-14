from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class IQuery:
    """Query interface."""


class BaseQuery(BaseModel, IQuery):
    """Base query."""
