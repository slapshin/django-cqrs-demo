import abc
import typing as ty

from apps.core import injector
from apps.core.logic.queries import IQuery
from apps.core.logic.queries.handler import (
    IQueryHandler,
    TQuery,
    TQueryHandler,
    TQueryResult,
)


class IQueryBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(self, query_handler: ty.Type[TQueryHandler]) -> None:
        """Register query handler."""

    @abc.abstractmethod
    def register_handlers(self, handlers: ty.Iterable[TQueryHandler]) -> None:
        """Register many query handlers."""

    @abc.abstractmethod
    def dispatch(self, query: IQuery[TQueryResult]) -> TQueryResult:
        """Send query and get result."""


class QueryBus(IQueryBus):
    """Queries dispatcher."""

    def __init__(self) -> None:
        """Initializing."""
        self._registry: dict[ty.Type[TQuery], ty.Type[TQueryHandler]] = {}

    def register_handler(self, query_handler: ty.Type[TQueryHandler]) -> None:
        """Register query handler."""
        query_type: IQuery[TQueryResult] | None = None
        for orig_base in query_handler.__orig_bases__:
            origin = ty.get_origin(orig_base)
            if origin and issubclass(origin, IQueryHandler):
                query_type = ty.get_args(orig_base)[0]

        if not query_type:
            raise ValueError(
                'Can\'t extract query from handler "{0}"'.format(
                    query_handler,
                ),
            )
        self._registry[query_type] = query_handler

    def register_handlers(
        self,
        handlers: ty.Iterable[ty.Type[TQueryHandler]],
    ) -> None:
        """Register many query handlers."""
        for query_handler in handlers:
            self.register_handler(query_handler)

    def dispatch(self, query: IQuery[TQueryResult]) -> TQueryResult:
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
