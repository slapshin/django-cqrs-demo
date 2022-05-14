from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class ICommand:
    """Command interface."""


class BaseCommand(BaseModel, ICommand):
    """Base command."""
