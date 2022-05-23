from apps.core.logic.interfaces import IEMailService


class EMailService(IEMailService):
    """Email message send interface."""

    def send_email(self, title: str) -> None:
        """Send email to user."""
