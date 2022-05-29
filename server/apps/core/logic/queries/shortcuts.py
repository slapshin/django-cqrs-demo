import typing as ty

from apps.core import injector
from apps.core.logic.queries import (
    IQuery,
    IQueryBus,
    TQueryHandler,
    TQueryResult,
)


def execute_query(query: IQuery[TQueryResult]):
    """Execute query."""
    query_bus = injector.get(IQueryBus)
    return query_bus.dispatch(query)


def register_queries(handlers: ty.Iterable[ty.Type[TQueryHandler]]):
    """Register queries handlers at injector."""
    injector.get(IQueryBus).register_handlers(handlers)
