import pytest

from apps.core.logic import commands
from apps.core.logic.errors import ValidationApplicationError
from apps.users.logic.commands import register
from tests.helpers.db import trigger_on_commit


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
        ValidationApplicationError,
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
        ValidationApplicationError,
        match="Passwords do not match",
    ):
        commands.execute_command(
            register.Command(
                email=user.email,
                password1="pass",
                password2="pass1",
            ),
        )


def test_email(db, mailoutbox):
    """Test email sending."""
    command_result = commands.execute_command(
        register.Command(
            email="user@mail.com",
            password1="passpass",
            password2="passpass",
        ),
    )
    user = command_result.user

    trigger_on_commit()

    assert len(mailoutbox) == 1

    email = mailoutbox[0]
    assert email.subject == "Successful registration"
    assert email.body == "You have successfully registered"
    assert email.to == [user.email]
