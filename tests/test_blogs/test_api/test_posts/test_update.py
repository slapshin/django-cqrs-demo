from http import HTTPStatus

from rest_framework.test import APIClient

from apps.blogs.models import Post
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(api_client: APIClient, user: User):
    """Test success."""
    post = PostFactory.create(author=user)
    api_client.force_login(user)
    response = api_client.patch(
        "/api/posts/{0}".format(post.id),
        data={
            "title": "my title",
            "content": "my content",
            "status": "draft",
        },
    )

    assert response.status_code == HTTPStatus.OK
    post = Post.objects.get(id=response.data["id"])
    assert post.title == "my title"
    assert post.content == "my content"


def test_not_auth(api_client: APIClient, user: User):
    """Test not auth."""
    post = PostFactory.create(author=user)
    response = api_client.patch(
        "/api/posts/{0}".format(post.id),
        data={
            "title": "my title",
            "content": "my content",
            "status": "draft",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
