import pytest

from tests.helpers.users import create_user

DEFAULT_USER_EMAIL = "user@mail.com"
DEFAULT_USER_PASSWORD = "password"  # noqa: S105
ANOTHER_USER_EMAIL = "another@mail.com"


@pytest.fixture()
def user(db):
    """User."""
    return create_user(
        email=DEFAULT_USER_EMAIL,
        password=DEFAULT_USER_PASSWORD,
    )


@pytest.fixture()
def another_user(db):
    """Another user."""
    return create_user(
        ANOTHER_USER_EMAIL,
        password=DEFAULT_USER_PASSWORD,
    )
