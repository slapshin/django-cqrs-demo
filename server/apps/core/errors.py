import abc


class BaseError(Exception, metaclass=abc.ABCMeta):
    """Base error for all errors in the application."""

    code: str
    message: str

    def __init__(self):
        """Initialize."""
        super().__init__(self.message)
