import pytest

from apps.core.domain.errors import AccessDeniedDomainError
from apps.core.services import messages
from apps.users.domain.commands import logout
from apps.users.models import User


def test_success(user: User):
    """Test success logout."""
    messages.dispatch_message(
        logout.Command(user_id=user.id),
    )


def test_not_user(user: User):
    """Test not user."""
    with pytest.raises(AccessDeniedDomainError):
        messages.dispatch_message(
            logout.Command(user_id=None),
        )
