import pytest

from apps.blogs.domain.commands.posts import delete as delete_command
from apps.blogs.models import Post
from apps.core.domain.errors import (
    AccessDeniedDomainError,
    ObjectNotFoundDomainError,
)
from apps.core.services import messages
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(user: User):
    """Test success post deletion."""
    post = PostFactory.create(author=user)
    messages.dispatch_message(
        delete_command.Command(
            user_id=user.id,
            post_id=post.id,
        ),
    )

    assert not Post.objects.filter(id=post.id).exists()


def test_not_owner(user: User, another_user: User):
    """Test not owner deletion."""
    post = PostFactory.create(author=another_user)

    with pytest.raises(AccessDeniedDomainError):
        messages.dispatch_message(
            delete_command.Command(
                user_id=user.id,
                post_id=post.id,
            ),
        )

    assert Post.objects.filter(id=post.id).exists()


def test_not_found(user: User):
    """Test not found."""
    post = PostFactory.create(author=user)

    with pytest.raises(ObjectNotFoundDomainError):
        messages.dispatch_message(
            delete_command.Command(
                user_id=user.id,
                post_id=post.id + 1,
            ),
        )

    assert Post.objects.filter(id=post.id).exists()


def test_not_user(user: User):
    """Test not user."""
    post = PostFactory.create(author=user)

    with pytest.raises(AccessDeniedDomainError):
        messages.dispatch_message(
            delete_command.Command(
                user_id=None,
                post_id=post.id,
            ),
        )

    assert Post.objects.filter(id=post.id).exists()
