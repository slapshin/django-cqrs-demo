from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.test_blogs.factories.post import PostFactory


def test_initial(client: Client, user: User):
    """Test initial page."""
    post = PostFactory.create(author=user)

    client.force_login(user)
    response = client.get("/posts/{0}/edit/".format(post.id))

    assert response.status_code == HTTPStatus.OK
    assert post.title in response.rendered_content
    assert post.content in response.rendered_content


def test_initial_not_auth(client: Client, user: User):
    """Test initial page not auth."""
    post = PostFactory.create(author=user)

    response = client.get("/posts/{0}/edit/".format(post.id))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"


def test_success(client: Client, user: User):
    """Test success update ."""
    post = PostFactory.create(author=user)

    client.force_login(user)
    response = client.post(
        "/posts/{0}/edit/".format(post.id),
        data={
            "title": "new title",
            "content": post.content,
            "status": post.status,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/posts/{0}/".format(post.id)

    post.refresh_from_db()
    assert post.title == "new title"


def test_not_auth(client: Client, user: User):
    """Test not auth user."""
    post = PostFactory.create(author=user)

    response = client.post(
        "/posts/{0}/edit/".format(post.id),
        data={
            "title": "new title",
            "content": post.content,
            "status": post.status,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"


def test_not_owner(client: Client, user: User, another_user: User):
    """Test not owner."""
    post = PostFactory.create(author=another_user)

    response = client.post(
        "/posts/{0}/edit/".format(post.id),
        data={
            "title": "new title",
            "content": post.content,
            "status": post.status,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"
