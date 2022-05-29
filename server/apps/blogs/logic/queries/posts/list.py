from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import queries


@dataclass(frozen=True)
class QueryResult:
    """Posts list result."""

    instances: models.QuerySet


class Query(queries.BaseQuery[QueryResult]):
    """Post list query."""

    author_id: int | None = None


class QueryHandler(queries.IQueryHandler[Query]):
    """Posts list query handler."""

    def ask(self, query: Query) -> QueryResult:
        """Handler."""
        posts = Post.objects.filter(status=PostStatus.PUBLISHED)

        if query.author_id is not None:
            posts = posts.filter(author_id=query.author_id)

        posts = posts.order_by("-created_at")

        return QueryResult(
            instances=posts,
        )
