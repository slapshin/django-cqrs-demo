from http import HTTPStatus

from rest_framework.test import APIClient

from apps.blogs.models import Post
from apps.users.models import User


def test_success(api_client: APIClient, user: User):
    """Test success."""
    api_client.force_login(user)
    response = api_client.post(
        "/api/posts",
        data={
            "title": "my title",
            "content": "my content",
            "status": "draft",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    post = Post.objects.get(id=response.data["id"])
    assert post.title == "my title"
    assert post.content == "my content"


def test_not_auth(api_client: APIClient, user: User):
    """Test not auth."""
    response = api_client.post(
        "/api/posts",
        data={
            "title": "my title",
            "content": "my content",
            "status": "draft",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
