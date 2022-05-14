import pytest

from apps.blogs.logic.commands.posts import create
from apps.blogs.models.enums import PostStatus
from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.models import User


def test_success(user: User):
    """Test success post creation."""
    command_result = commands.execute_command(
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
    with pytest.raises(AccessDeniedApplicationError):
        commands.execute_command(
            create.Command(
                user_id=None,
                title="post title",
                content="post content",
                status=PostStatus.PUBLISHED,
            ),
        )
