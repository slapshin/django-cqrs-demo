from http import HTTPStatus

from django.test import Client

from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_initial(client: Client):
    """Test register form."""
    response = client.get("/registration")
    assert response.status_code == HTTPStatus.OK


def test_success(client: Client, db):
    """Test success registration."""
    response = client.post(
        "/registration",
        data={
            "email": "user@mail.com",
            "password1": DEFAULT_USER_PASSWORD,
            "password2": DEFAULT_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/"

    user = User.objects.filter(email="user@mail.com").first()
    assert user
    assert int(client.session.get("_auth_user_id")) == user.id


def test_user_already_exists(client: Client, user: User):
    """Test user already exists."""
    response = client.post(
        "/registration",
        data={
            "email": user.email,
            "password1": DEFAULT_USER_PASSWORD,
            "password2": DEFAULT_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert "User with this Email already exists" in response.rendered_content
