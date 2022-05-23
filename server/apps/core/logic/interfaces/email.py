import abc


class IEMailService(abc.ABC):
    """Email message send interface."""

    @abc.abstractmethod
    def send_email(self, title: str) -> None:
        """Send email to user."""
