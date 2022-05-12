from apps.core import injector
from apps.core.logic.queries import IQuery, IQueryBus
from apps.core.logic.queries.bus import QueryInfo


def execute_query(query: IQuery):
    """Execute query."""
    query_bus = injector.get(IQueryBus)
    return query_bus.dispatch(query)

def register_queries(handlers: list[QueryInfo]):
    injector.get(IQueryBus).register_many(handlers)
