import pytest

from apps.core.logic import bus
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.users.logic.commands import logout
from apps.users.models import User


def test_success(user: User):
    """Test success logout."""
    bus.dispatch_message(
        logout.Command(user_id=user.id),
    )


def test_not_user(user: User):
    """Test not user."""
    with pytest.raises(AccessDeniedApplicationError):
        bus.dispatch_message(
            logout.Command(user_id=None),
        )
