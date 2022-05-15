from http import HTTPStatus

from rest_framework.test import APIClient

from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_success(api_client: APIClient, user: User):
    """Test success login."""
    response = api_client.post(
        "/api/login",
        data={
            "username": user.email,
            "password": DEFAULT_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert int(api_client.session.get("_auth_user_id")) == user.id


def test_bad_username(api_client: APIClient, user: User):
    """Test bad username."""
    response = api_client.post(
        "/api/login",
        data={
            "username": "bad_{0}".format(user.email),
            "password": DEFAULT_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert not api_client.session.get("_auth_user_id")


def test_param_missing(api_client: APIClient, user: User):
    """Test username is missing."""
    response = api_client.post(
        "/api/login",
        data={
            "username": user.email,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
