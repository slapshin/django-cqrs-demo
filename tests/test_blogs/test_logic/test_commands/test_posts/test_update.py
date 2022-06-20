import pytest

from apps.blogs.logic.commands.posts import update
from apps.blogs.models.enums import PostStatus
from apps.core.logic import bus
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    ObjectNotFoundApplicationError,
)
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(user: User):
    """Test success post update."""
    post = PostFactory.create(author=user)

    bus.dispatch_message(
        update.Command(
            user_id=user.id,
            post_id=post.id,
            title="new title",
            content="new content",
            status=PostStatus.DRAFT,
        ),
    )

    post.refresh_from_db()

    assert post.title == "new title"
    assert post.content == "new content"
    assert post.status == PostStatus.DRAFT


def test_not_author(user: User, another_user: User):
    """Test user not author."""
    post = PostFactory.create(author=another_user)

    with pytest.raises(AccessDeniedApplicationError):
        bus.dispatch_message(
            update.Command(
                user_id=user.id,
                post_id=post.id,
                title="new title",
                content="new content",
                status=PostStatus.DRAFT,
            ),
        )


def test_not_found(user: User):
    """Test post not found."""
    post = PostFactory.create(author=user)

    with pytest.raises(ObjectNotFoundApplicationError):
        bus.dispatch_message(
            update.Command(
                user_id=user.id,
                post_id=post.id + 1,
                title="new title",
                content="new content",
                status=PostStatus.DRAFT,
            ),
        )


def test_not_user(user: User):
    """Test not user."""
    post = PostFactory.create(author=user)

    with pytest.raises(AccessDeniedApplicationError):
        bus.dispatch_message(
            update.Command(
                user_id=None,
                post_id=post.id,
                title="new title",
                content="new content",
                status=PostStatus.DRAFT,
            ),
        )
