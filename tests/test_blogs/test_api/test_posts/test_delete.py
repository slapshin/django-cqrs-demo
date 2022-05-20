from http import HTTPStatus

from rest_framework.test import APIClient

from apps.blogs.models import Post
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(api_client: APIClient, user: User):
    """Test success."""
    post = PostFactory.create(author=user)

    api_client.force_login(user)
    response = api_client.delete("/api/posts/{0}".format(post.id))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Post.objects.filter(id=post.id).exists()


def test_no_auth(api_client: APIClient, db):
    """Test no auth."""
    post = PostFactory.create()

    response = api_client.delete("/api/posts/{0}".format(post.id))

    assert response.status_code == HTTPStatus.FORBIDDEN
