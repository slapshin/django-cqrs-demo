from dataclasses import dataclass

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.logic import messages
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


@dataclass(frozen=True)
class CommandResult:
    """Register output dto."""

    user: User


class Command(messages.BaseCommand[CommandResult]):
    """Register command."""

    email: str
    password1: str
    password2: str


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Register new user."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        self._validate_command(command)
        user = self._create_user(command)

        messages.dispatch_message_async(
            send_registration_notification.Command(user_id=user.id),
        )

        return CommandResult(
            user=user,
        )

    def _validate_command(self, command: Command) -> None:
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

    def _create_user(self, command: Command) -> User:
        user = User(
            email=command.email,
            last_login=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        user.set_password(command.password1)
        user.full_clean()
        user.save()

        return user
