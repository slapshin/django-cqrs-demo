import abc

from apps.users.models import User


class IAuthenticationService(abc.ABC):
    """User login service."""

    @abc.abstractmethod
    def auth(self, email: str, password: str) -> User | None:
        """Login user by provided credentials."""
