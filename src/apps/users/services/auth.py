from django.contrib.auth import authenticate

from apps.users.logic.interfaces import IAuthenticationService
from apps.users.models import User


class AuthenticationService(IAuthenticationService):
    """Login service."""

    def auth(self, email: str, password: str) -> User | None:
        """Login user by provided credentials."""
        return authenticate(email=email, password=password)
