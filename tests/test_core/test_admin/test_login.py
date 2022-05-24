from http import HTTPStatus

import pytest
from django.test import Client

from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


@pytest.fixture()
def admin_client() -> Client:
    """Init admin client."""
    return Client()


def test_login(user: User, admin_client: Client):
    """Test login in main admin form."""
    user.is_staff = True
    user.set_password(DEFAULT_USER_PASSWORD)
    user.save()

    response = admin_client.post(
        "/admin/login/?next=/admin/",
        data={
            "username": user.email,
            "password": DEFAULT_USER_PASSWORD,
        },
        follow=True,
    )

    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
