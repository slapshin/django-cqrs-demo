import abc
import typing as ty

from apps.core.logic.queries import IQuery

TQuery = ty.TypeVar("TQuery", bound=IQuery)
TResult = ty.TypeVar("TResult")


class IQueryHandler(ty.Generic[TQuery, TResult], metaclass=abc.ABCMeta):
    """Base command handler."""

    @abc.abstractmethod
    def ask(self, query: TQuery) -> TResult:
        """Main logic here."""
