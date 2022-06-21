import pytest

from apps.blogs.logic.queries.posts import my as my_query
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_all(user: User, another_user: User):
    """Test success."""
    PostFactory.create_batch(3, author=another_user)
    PostFactory.create_batch(3, author=user)

    query_result = messages.dispatch_message(
        my_query.Query(
            user_id=user.id,
        ),
    )

    assert query_result.instances.count() == 3


def test_not_user(user: User, another_user: User):
    """Test not user provided."""
    PostFactory.create_batch(3, author=another_user)
    PostFactory.create_batch(1, author=user)

    with pytest.raises(AccessDeniedApplicationError):
        messages.dispatch_message(
            my_query.Query(
                user_id=None,
            ),
        )


def test_draft(user: User):
    """Test draft post."""
    PostFactory.create_batch(2, author=user, status=PostStatus.DRAFT)
    PostFactory.create_batch(3, author=user)

    query_result = messages.dispatch_message(
        my_query.Query(
            user_id=user.id,
        ),
    )

    assert query_result.instances.count() == 5
