from http import HTTPStatus

from rest_framework.test import APIClient

from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_EMAIL


def test_success(api_client: APIClient, db):
    """Test success registration."""
    response = api_client.post(
        "/api/register",
        data={
            "email": DEFAULT_USER_EMAIL,
            "password1": "passpass",
            "password2": "passpass",
        },
    )

    assert response.status_code == HTTPStatus.OK
    user = User.objects.filter(email=DEFAULT_USER_EMAIL).first()
    assert user
    assert int(api_client.session.get("_auth_user_id")) == user.id


def test_user_exists(api_client: APIClient, user: User):
    """Test user exists."""
    response = api_client.post(
        "/api/register",
        data={
            "email": DEFAULT_USER_EMAIL,
            "password1": "passpass",
            "password2": "passpass",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_param_missing(api_client: APIClient, user: User):
    """Test username is missing."""
    response = api_client.post(
        "/api/register",
        data={
            "username": user.email,
            "password1": "passpass",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
