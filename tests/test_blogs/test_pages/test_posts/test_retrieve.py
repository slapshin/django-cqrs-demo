from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(client: Client, user: User):
    """Test success retrieve."""
    post = PostFactory.create(author=user)

    response = client.get("/posts/{0}/".format(post.id))

    assert response.status_code == HTTPStatus.OK
    assert post.title in response.rendered_content


def test_not_found(client: Client, user: User):
    """Test not found."""
    post = PostFactory.create(author=user)

    response = client.get("/posts/{0}/".format(post.id + 1))

    assert response.status_code == HTTPStatus.OK
    assert "Post not found" in response.rendered_content
