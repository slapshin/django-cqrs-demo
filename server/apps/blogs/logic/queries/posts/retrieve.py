from dataclasses import dataclass

from django.db import models

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages
from apps.core.logic.errors import AccessDeniedApplicationError


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

    def execute(self, message: Query) -> QueryResult:
        """Handler."""
        if message.only_owner and not message.user_id:
            raise AccessDeniedApplicationError()

        return QueryResult(
            instance=self._get_post(message),
        )

    def _get_post(self, message: Query) -> Post | None:
        posts = Post.objects.all()
        if message.user_id:
            posts = posts.filter(
                models.Q(status=PostStatus.PUBLISHED)
                | models.Q(
                    status=PostStatus.DRAFT,
                    author_id=message.user_id,
                ),
            )
        else:
            posts = posts.filter(models.Q(status=PostStatus.PUBLISHED))

        post = posts.filter(id=message.post_id).first()
        if post and not self._is_post_allowed(post, message):
            return None

        return post

    def _is_post_allowed(self, post: Post, query: Query) -> bool:
        return not query.only_owner or (post.author_id == query.user_id)
