import abc


class IEMailService(abc.ABC):
    """Email message send interface."""

    @abc.abstractmethod
    def send_email(
        self,
        subject: str,
        message: str,
        to: str,
    ) -> None:
        """Send email to user."""
