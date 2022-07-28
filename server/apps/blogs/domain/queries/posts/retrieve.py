from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.domain import messages
from apps.core.domain.errors import AccessDeniedDomainError


@dataclass(frozen=True)
class QueryResult:
    """Post retrieve result."""

    instance: Post | None


class Query(messages.BaseQuery[QueryResult]):
    """Post retrieve query."""

    post_id: int
    user_id: int | None = None
    only_owner: bool = False


class QueryHandler(messages.BaseQueryHandler[Query]):
    """Post retrieve query handler."""

    def handle(self, query: Query) -> QueryResult:
        """Handler."""
        if query.only_owner and not query.user_id:
            raise AccessDeniedDomainError()

        return QueryResult(
            instance=self._get_post(query),
        )

    def _get_post(self, query: Query) -> Post | None:
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

        post = posts.filter(id=query.post_id).first()
        if post and not self._is_post_allowed(post, query):
            return None

        return post

    def _is_post_allowed(self, post: Post, query: Query) -> bool:
        return not query.only_owner or (post.author_id == query.user_id)
