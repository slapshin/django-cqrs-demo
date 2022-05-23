from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.core.logic.interfaces import IEMailService


class EMailService(IEMailService):
    """Email message send interface."""

    def send_email(
        self,
        subject: str,
        message: str,
        to: str,
    ) -> None:
        """Send email to user."""
        html_message = render_to_string(
            "email.html",
            context={"message": message},
        )
        send_mail(
            subject,
            message=message,
            html_message=html_message,
            from_email=None,
            recipient_list=[to],
            fail_silently=False,
        )
