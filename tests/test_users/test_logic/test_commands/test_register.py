import pytest
from django.core.exceptions import ValidationError as DjangoValidationError
from pydantic import ValidationError

from apps.core.logic import commands
from apps.users.logic.commands import register


def test_success(db):
    """Test success registration."""
    command_result = commands.execute_command(
        register.Command(
            email="user@mail.com",
            password1="passpass",
            password2="passpass",
        ),
    )
    user = command_result.user

    assert user.email == "user@mail.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_user_already_exists(user):
    """Test user already exists."""
    with pytest.raises(register.UserAlreadyExistsError):
        commands.execute_command(
            register.Command(
                email=user.email,
                password1="passpass",
                password2="passpass",
            ),
        )


def test_short_password(user):
    """Test short password."""
    with pytest.raises(
        DjangoValidationError,
        match="This password is too short",
    ):
        commands.execute_command(
            register.Command(
                email=user.email,
                password1="pass",
                password2="pass",
            ),
        )


def test_passwords_not_matched(user):
    """Test passwords are not matched."""
    with pytest.raises(
        ValidationError,
        match="Passwords do not match",
    ):
        commands.execute_command(
            register.Command(
                email=user.email,
                password1="pass",
                password2="pass1",
            ),
        )
