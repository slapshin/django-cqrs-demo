from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.core.logic import messages
from apps.core.logic.errors import AccessDeniedApplicationError


@dataclass(frozen=True)
class QueryResult:
    """User posts list result."""

    instances: models.QuerySet


class Query(messages.BaseQuery[QueryResult]):
    """User posts list."""

    user_id: int | None


class QueryHandler(messages.BaseQueryHandler[Query]):
    """User posts list query handler."""

    def handle(self, query: Query) -> QueryResult:
        """Handler."""
        if not query.user_id:
            raise AccessDeniedApplicationError()

        posts = Post.objects.filter(
            author_id=query.user_id,
        ).order_by("-created_at")

        return QueryResult(
            instances=posts,
        )
