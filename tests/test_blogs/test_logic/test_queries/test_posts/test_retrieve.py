from apps.blogs.logic.queries.posts import retrieve as retrieve_query
from apps.blogs.models.enums import PostStatus
from apps.core.logic import messages
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(user: User):
    """Test success."""
    post = PostFactory.create(author=user)

    query_result = messages.dispatch_message(
        retrieve_query.Query(
            user_id=user.id,
            post_id=post.id,
        ),
    )

    assert query_result.instance.title == post.title
    assert query_result.instance.id == post.id


def test_draft(user: User, another_user: User):
    """Test draft."""
    post = PostFactory.create(
        author=another_user,
        status=PostStatus.DRAFT,
    )

    query_result = messages.dispatch_message(
        retrieve_query.Query(
            user_id=user.id,
            post_id=post.id,
        ),
    )

    assert not query_result.instance


def test_draft_and_author(user: User):
    """Test draft and author."""
    post = PostFactory.create(
        author=user,
        status=PostStatus.DRAFT,
    )

    query_result = messages.dispatch_message(
        retrieve_query.Query(
            user_id=user.id,
            post_id=post.id,
        ),
    )

    assert query_result.instance.id == post.id


def test_only_owner(user: User, another_user: User):
    """Test only owner."""
    post = PostFactory.create(author=another_user)

    query_result = messages.dispatch_message(
        retrieve_query.Query(
            user_id=user.id,
            post_id=post.id,
            only_owner=True,
        ),
    )

    assert not query_result.instance
