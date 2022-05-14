from apps.users.models import User


def create_user(email: str, password: str) -> User:
    """Create or returns user."""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return User.objects.create_user(
            email=email,
            password=password,
        )
