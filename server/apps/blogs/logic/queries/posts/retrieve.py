from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import queries
from apps.core.logic.errors import AccessDeniedApplicationError


@dataclass(frozen=True)
class Query(queries.IQuery):
    """Post list."""

    post_id: int
    user_id: int | None = None
    only_owner: bool = False


@dataclass(frozen=True)
class QueryResult:
    """Post retrieve result."""

    instance: Post | None


class QueryHandler(queries.IQueryHandler[Query, QueryResult]):
    """Post retrieve query handler."""

    def ask(self, query: Query) -> QueryResult:
        """Handler."""
        if query.only_owner and not query.user_id:
            raise AccessDeniedApplicationError()

        posts = Post.objects.all()
        if query.user_id:
            posts = posts.filter(
                models.Q(status=PostStatus.PUBLISHED)
                | models.Q(
                    status=PostStatus.DRAFT,
                    author_id=query.user_id,
                )
            )
        else:
            posts = posts.filter(models.Q(status=PostStatus.PUBLISHED))

        post = posts.filter(id=query.post_id).first()
        if post and query.only_owner and post.author_id != query.user_id:
            raise AccessDeniedApplicationError()

        return QueryResult(
            instance=post,
        )
