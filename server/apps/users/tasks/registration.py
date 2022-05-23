from celery import shared_task


@shared_task
def send_registration_email_task(user_id: str):
    """Send registration emial."""
