from dataclasses import dataclass

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.logic import commands
from apps.core.logic.errors import (
    BaseApplicationError,
    ValidationApplicationError,
)
from apps.users.logic.commands import send_registration_notification
from apps.users.models import User


class BaseRegistrationError(BaseApplicationError):
    """Base registration error."""


class UserAlreadyExistsError(BaseRegistrationError):
    """User already exists error."""

    code = "user_already_exists"
    message = _("MSG__USER_ALREADY_EXISTS")


class Command(commands.BaseCommand):
    """Register command."""

    email: str
    password1: str
    password2: str


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    user: User


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Register new user."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        self._validate_data(command)

        user = User(
            email=command.email,
            last_login=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        user.set_password(command.password1)
        user.full_clean()
        user.save()

        commands.execute_command(
            send_registration_notification.Command(user_id=user.id),
        )
        return CommandResult(
            user=user,
        )

    def _validate_data(self, command: Command) -> None:
        """Validate input data."""
        if command.password1 != command.password2:
            raise ValidationApplicationError(
                {"password2": ["Passwords do not match"]},
            )

        try:
            password_validation.validate_password(command.password1)
        except ValidationError as err:
            raise ValidationApplicationError(
                {
                    "password1": err.messages,
                },
            )

        if User.objects.filter(email=command.email).exists():
            raise UserAlreadyExistsError()
