import abc
from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True)
class SignupData:
    """Data to create user."""

    name: str
    password: str
    email: str


class ISignupService(abc.ABC):
    """Signup user interface."""

    @abc.abstractmethod
    def signup(self, signup_data: SignupData) -> User:
        """Signup user by provided data."""
