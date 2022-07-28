import abc
import pprint

from django.utils.translation import gettext_lazy as _

from apps.core.errors import BaseError


class BaseDomainError(BaseError, metaclass=abc.ABCMeta):
    """Base exception for application errors."""

    def __init__(
        self,
        code: str | None = None,
        message: str | None = None,
    ) -> None:
        """Initializing."""
        if code:
            self.code = code
        if message:
            self.message = message

        super().__init__()


class ValidationDomainError(BaseError, metaclass=abc.ABCMeta):
    """
    Invalid input error.

    The error represents invalid input data information.
    """

    code = "invalid_input"
    message = _("MSG__INVALID_INPUT")

    def __init__(self, errors: dict[str, list[str] | str]) -> None:
        """Initialize with input errors."""
        super().__init__()
        self.errors = errors

    def __str__(self) -> str:
        """String presentation."""
        return pprint.pformat(self.errors, indent=2)


class AccessDeniedDomainError(BaseDomainError):
    """
    Access forbidden error.

    User has no permissions to execute the action.
    """

    code = "operation_not_permitted"
    message = _("MSG__OPERATION_NOT_PERMITTED")


class UnauthenticatedDomainError(BaseDomainError):
    """
    User unauthenticated application error.

    The action requires user, but no user was provided.
    """

    code = "authentication_required"
    message = _("MSG__OPERATION_NOT_PERMITTED")


class AuthenticationDomainError(BaseDomainError):
    """
    Authentication error.

    Can't authenticate the user.
    """

    code = "authentication_error"
    message = _("MSG__AUTHENTICATION_ERROR")


class ObjectNotFoundDomainError(BaseDomainError):
    """
    Resource not found error.

    If query/command handler can't get object need to process action.
    """

    code = "not_found_error"
    message = _("MSG__NOT_FOUND_ERROR")
