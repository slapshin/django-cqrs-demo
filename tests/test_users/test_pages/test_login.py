from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_initial(client: Client):
    """Test login form."""
    response = client.get("/login")
    assert response.status_code == HTTPStatus.OK


def test_success(client: Client, user: User):
    """Test success login."""
    response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": DEFAULT_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/"
    assert int(client.session.get("_auth_user_id")) == user.id


def test_wrong_password(client: Client, user: User):
    """Test wrong password."""
    response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": "bad{0}".format(DEFAULT_USER_PASSWORD),
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert "Invalid username or password" in response.rendered_content
