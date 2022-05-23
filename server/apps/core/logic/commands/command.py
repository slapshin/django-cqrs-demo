import abc

from pydantic import BaseModel


class ICommand:
    """Command interface."""

    @classmethod
    def deserialize(cls, string_data: str) -> "ICommand":
        """Deserialize object."""

    def serialize(self) -> str:
        """Serialize object."""


class BaseCommand(BaseModel, ICommand, metaclass=abc.ABCMeta):
    """Base command."""

    @classmethod
    def deserialize(cls, string_data: str) -> "ICommand":
        """Deserialize object."""
        return cls.parse_raw(string_data)

    def serialize(self) -> str:
        """Serialize object."""
        return self.json()
