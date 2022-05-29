import abc
import typing as ty

from apps.core.logic.queries import IQuery
from apps.core.logic.queries.query import TQueryResult

TQuery = ty.TypeVar("TQuery", bound=IQuery[TQueryResult])


class IQueryHandler(
    ty.Generic[TQuery],
    metaclass=abc.ABCMeta,
):
    """Base query handler."""

    @abc.abstractmethod
    def ask(self, query: TQuery) -> TQueryResult:
        """Main logic here."""


TQueryHandler = ty.TypeVar(
    "TQueryHandler",
    bound=IQueryHandler[IQuery[TQueryResult]],
)
