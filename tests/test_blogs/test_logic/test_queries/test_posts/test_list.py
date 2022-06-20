from apps.blogs.logic.queries.posts import list as list_query
from apps.blogs.models.enums import PostStatus
from apps.core.logic import bus
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_all(user: User, another_user: User):
    """Test success."""
    PostFactory.create_batch(3, author=another_user)
    PostFactory.create_batch(3, author=user)

    query_result = bus.dispatch_message(list_query.Query())

    assert query_result.instances.count() == 6


def test_specific_author(user: User, another_user: User):
    """Test specific user."""
    PostFactory.create_batch(1, author=another_user)
    PostFactory.create_batch(3, author=user)

    query_result = bus.dispatch_message(
        list_query.Query(
            author_id=user.id,
        ),
    )

    assert query_result.instances.count() == 3


def test_draft(user: User):
    """Test draft post."""
    PostFactory.create_batch(2, author=user, status=PostStatus.DRAFT)
    PostFactory.create_batch(3, author=user)

    query_result = bus.dispatch_message(list_query.Query())

    assert query_result.instances.count() == 3


def test_draft_and_author(user: User):
    """Test draft post and author."""
    PostFactory.create_batch(2, author=user, status=PostStatus.DRAFT)
    PostFactory.create_batch(3, author=user)

    query_result = bus.dispatch_message(
        list_query.Query(
            author_id=user.id,
        ),
    )

    assert query_result.instances.count() == 3
