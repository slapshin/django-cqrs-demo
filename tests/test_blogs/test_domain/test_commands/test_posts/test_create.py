import pytest

from apps.blogs.domain.commands.posts import create
from apps.blogs.models.enums import PostStatus
from apps.core.domain.errors import AccessDeniedDomainError
from apps.core.services import messages
from apps.users.models import User


def test_success(user: User):
    """Test success post creation."""
    command_result = messages.dispatch_message(
        create.Command(
            user_id=user.id,
            title="post title",
            content="post content",
            status=PostStatus.PUBLISHED,
        ),
    )

    post = command_result.instance

    assert post.title == "post title"
    assert post.content == "post content"
    assert post.status == PostStatus.PUBLISHED


def test_not_user(db):
    """Test not user."""
    with pytest.raises(AccessDeniedDomainError):
        messages.dispatch_message(
            create.Command(
                user_id=None,
                title="post title",
                content="post content",
                status=PostStatus.PUBLISHED,
            ),
        )
