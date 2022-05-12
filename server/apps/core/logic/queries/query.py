from dataclasses import dataclass


@dataclass(frozen=True)
class IQuery:
    """Query interface."""
