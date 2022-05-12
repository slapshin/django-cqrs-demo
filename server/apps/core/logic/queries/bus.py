import abc
import typing as ty

from apps.core import injector
from apps.core.logic.queries import IQuery
from apps.core.logic.queries.handler import IQueryHandler, TResult

QueryInfo = ty.Tuple[
    ty.Type[IQuery],
    ty.Type[IQueryHandler[IQuery, TResult]],
]


class IQueryBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register(
        self,
        query_type: ty.Type[IQuery],
        query_handler: ty.Type[IQueryHandler[IQuery, TResult]],
    ) -> None:
        """Register query handler."""

    @abc.abstractmethod
    def register_many(self, handlers: list[QueryInfo]) -> None:
        """Register many query handlers."""

    @abc.abstractmethod
    def dispatch(self, query: IQuery) -> TResult:
        """Send query and get result."""


class QueryBus(IQueryBus):
    """Queries dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register(
        self,
        query_type: ty.Type[IQuery],
        query_handler: ty.Type[IQueryHandler[IQuery, TResult]],
    ) -> None:
        """Register command handler."""
        self._registry[query_type] = query_handler

    def register_many(self, handlers: list[QueryInfo]) -> None:
        """Register many query handlers."""
        for query, query_handler in handlers:
            self.register(query, query_handler)

    def dispatch(self, query: IQuery) -> TResult:
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(query))
        if not handler_type:
            raise ValueError(
                'Handler for query "{0}" is not registered'.format(
                    type(query),
                ),
            )
        query_handler = injector.get(handler_type)
        return query_handler.ask(query)
