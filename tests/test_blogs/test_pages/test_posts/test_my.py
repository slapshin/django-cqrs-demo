from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_all(client: Client, user: User, another_user: User):
    """Test home page."""
    my_posts = PostFactory.create_batch(3, author=user)
    other_posts = PostFactory.create_batch(2, author=another_user)

    client.force_login(user)
    response = client.get("/posts/my/")

    assert response.status_code == HTTPStatus.OK
    for post in my_posts:
        assert post.title in response.rendered_content

    for other_post in other_posts:
        assert other_post.title not in response.rendered_content


def test_not_auth(client: Client, user: User):
    """Test not auth."""
    PostFactory.create_batch(3, author=user)

    response = client.get("/posts/my/")

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"
