from http import HTTPStatus

from rest_framework.test import APIClient

from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(api_client: APIClient, user: User):
    """Test success."""
    post = PostFactory.create()

    response = api_client.get("/api/posts/{0}".format(post.id))

    assert response.status_code == HTTPStatus.OK
    assert response.data["id"] == post.id
