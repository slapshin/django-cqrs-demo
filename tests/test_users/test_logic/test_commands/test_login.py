import pytest

from apps.core.logic import bus
from apps.core.logic.errors import AuthenticationApplicationError
from apps.users.logic.commands import login
from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_success(user: User):
    """Test success auth."""
    command_result = bus.dispatch_message(
        login.Command(
            username=user.email,
            password=DEFAULT_USER_PASSWORD,
        ),
    )

    assert command_result.user == user


def test_bad_username(user: User):
    """Test wrong username."""
    with pytest.raises(AuthenticationApplicationError):
        bus.dispatch_message(
            login.Command(
                username="bad_{0}".format(user.email),
                password=DEFAULT_USER_PASSWORD,
            ),
        )


def test_bad_password(user: User):
    """Test wrong password."""
    with pytest.raises(AuthenticationApplicationError):
        bus.dispatch_message(
            login.Command(
                username=user.email,
                password="bad_{0}".format(DEFAULT_USER_PASSWORD),
            ),
        )
