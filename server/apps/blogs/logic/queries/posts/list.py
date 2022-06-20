from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages


@dataclass(frozen=True)
class QueryResult:
    """Posts list result."""

    instances: models.QuerySet


class Query(messages.BaseMessage[QueryResult]):
    """Post list query."""

    author_id: int | None = None


class QueryHandler(messages.IMessageHandler[Query]):
    """Posts list query handler."""

    def execute(self, message: Query) -> QueryResult:
        """Handler."""
        posts = Post.objects.filter(status=PostStatus.PUBLISHED)

        if message.author_id is not None:
            posts = posts.filter(author_id=message.author_id)

        posts = posts.order_by("-created_at")

        return QueryResult(
            instances=posts,
        )
