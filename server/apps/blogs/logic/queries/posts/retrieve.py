from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import queries
from apps.core.logic.errors import AccessDeniedApplicationError


@dataclass(frozen=True)
class Query(queries.IQuery):
    """Post retrieve query."""

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

        posts = self._build_posts_query(query)
        post = posts.filter(id=query.post_id).first()

        self._check_if_post_allowed(query, post)

        return QueryResult(
            instance=post,
        )

    def _build_posts_query(self, query: Query) -> models.QuerySet:
        posts = Post.objects.all()
        if query.user_id:
            posts = posts.filter(
                models.Q(status=PostStatus.PUBLISHED)
                | models.Q(
                    status=PostStatus.DRAFT,
                    author_id=query.user_id,
                ),
            )
        else:
            posts = posts.filter(models.Q(status=PostStatus.PUBLISHED))

        return posts

    def _check_if_post_allowed(self, query: Query, post: Post | None):
        is_allowed = (
            not post
            or not query.only_owner
            or (post.author_id == query.user_id)
        )
        if not is_allowed:
            raise AccessDeniedApplicationError()
