from dataclasses import dataclass


@dataclass
class Pagination:
    """Pagination fields."""

    page_size: int | None = None
    page_number: int | None = 1
