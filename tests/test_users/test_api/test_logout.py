from http import HTTPStatus

from rest_framework.test import APIClient

from apps.users.models import User


def test_success(api_client: APIClient, user: User):
    """Test success logout."""
    api_client.force_login(user)
    response = api_client.post("/api/logout")
    assert response.status_code == HTTPStatus.OK
    assert not api_client.session.get("_auth_user_id")


def test_not_auth(api_client: APIClient, user: User):
    """Test not auth."""
    response = api_client.post("/api/logout")
    assert response.status_code == HTTPStatus.FORBIDDEN
