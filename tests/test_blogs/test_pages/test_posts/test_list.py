from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_all(client: Client, user: User, another_user: User):
    """Test home page."""
    posts = (
        *PostFactory.create_batch(3, author=user),
        *PostFactory.create_batch(2, author=another_user),
    )

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    for post in posts:
        assert post.title in response.rendered_content
