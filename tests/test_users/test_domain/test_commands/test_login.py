import pytest

from apps.core.domain.errors import AuthenticationDomainError
from apps.core.services import messages
from apps.users.domain.commands import login
from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_success(user: User):
    """Test success auth."""
    command_result = messages.dispatch_message(
        login.Command(
            username=user.email,
            password=DEFAULT_USER_PASSWORD,
        ),
    )

    assert command_result.user == user


def test_bad_username(user: User):
    """Test wrong username."""
    with pytest.raises(AuthenticationDomainError):
        messages.dispatch_message(
            login.Command(
                username="bad_{0}".format(user.email),
                password=DEFAULT_USER_PASSWORD,
            ),
        )


def test_bad_password(user: User):
    """Test wrong password."""
    with pytest.raises(AuthenticationDomainError):
        messages.dispatch_message(
            login.Command(
                username=user.email,
                password="bad_{0}".format(DEFAULT_USER_PASSWORD),
            ),
        )
