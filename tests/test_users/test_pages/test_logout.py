from http import HTTPStatus

from django.test import Client

from apps.users.models import User


def test_success(client: Client, user: User):
    """Test success."""
    client.force_login(user)
    response = client.post("/logout/")
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/"
    assert not client.session.get("_auth_user_id")


def test_not_auth(client: Client):
    """Test not auth."""
    response = client.post("/logout/")
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/"
