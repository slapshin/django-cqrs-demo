from http import HTTPStatus

from django.test import Client

from apps.blogs.models import Post
from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_success(client: Client, user: User):
    """Test success update ."""
    post = PostFactory.create(author=user)

    client.force_login(user)
    response = client.post("/posts/{0}/delete/".format(post.id))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/posts/my/"
    assert not Post.objects.filter(id=post.id).exists()


def test_not_auth(client: Client, user: User):
    """Test not auth user."""
    post = PostFactory.create(author=user)

    response = client.post("/posts/{0}/delete/".format(post.id))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"


def test_not_owner(client: Client, user: User, another_user: User):
    """Test not owner."""
    post = PostFactory.create(author=another_user)

    client.force_login(user)
    response = client.post("/posts/{0}/delete/".format(post.id))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"
