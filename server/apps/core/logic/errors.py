import abc

from django.utils.translation import gettext_lazy as _

from apps.core.errors import BaseError


class BaseApplicationError(BaseError, metaclass=abc.ABCMeta):
    """Base exception for application errors."""

    def __init__(
        self,
        code: str | None = None,
        message: str | None = None,
    ):
        """Initizaling."""
        if code:
            self.code = code
        if message:
            self.message = message

        super().__init__()


class AuthenticationErrorMixin(BaseApplicationError):
    """Mark the error as authentication error."""


class AccessDeniedErrorMixin(BaseApplicationError):
    """Mark the error as forbidden error."""


class InvalidInputApplicationError(BaseError, metaclass=abc.ABCMeta):
    """Invalid input error."""

    code = "invalid_input"
    message = _("MSG__INVALID_INPUT")

    def __init__(self, errors):
        """Initialize with input errors."""
        super().__init__()
        self.errors = errors


class AccessDeniedApplicationError(AccessDeniedErrorMixin):
    """Mark the error as forbid error."""

    code = "operation_not_permitted"
    message = _("MSG__OPERATION_NOT_PERMITTED")


class AuthenticationErrorApplicationError(AuthenticationErrorMixin):
    """Mark the error as auth error."""

    code = "authentication_error"
    message = _("MSG__AUTHENTICATION_ERROR")


class ObjectNotFoundError(BaseApplicationError):
    """Mark the error as not_found error."""

    code = "not_found_error"
    message = _("MSG__NOT_FOUND_ERROR")
