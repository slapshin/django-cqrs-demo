import pytest

from apps.core.logic import commands
from apps.users.logic.commands import login
from tests.fixtures.users import DEFAULT_USER_PASSWORD


def test_success(user):
    """Test success auth."""
    command_result = commands.execute_command(
        login.Command(
            username=user.email,
            password=DEFAULT_USER_PASSWORD,
        ),
    )

    assert command_result.user == user


def test_bad_username(user):
    """Test wrong username."""
    with pytest.raises(ValueError, match="Invalid username or password"):
        commands.execute_command(
            login.Command(
                username="bad_{0}".format(user.email),
                password=DEFAULT_USER_PASSWORD,
            ),
        )


def test_bad_password(user):
    """Test wrong password."""
    with pytest.raises(ValueError, match="Invalid username or password"):
        commands.execute_command(
            login.Command(
                username=user.email,
                password="bad_{0}".format(DEFAULT_USER_PASSWORD),
            ),
        )
