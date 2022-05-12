from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import Token
from apps.users.services.token import create_user_token


def login_user(login: str, password: str, request=None) -> Token:
    """Login user."""
    if login and password:
        user = authenticate(request=request, login=login, password=password)

        if not user:
            raise AuthenticationFailed(
                _("MSG_UNABLE_TO_LOGIN_WITH_PROVIDED_CREDENTIALS"),
            )

        token = create_user_token(user)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return token  # noqa: WPS331

    raise AuthenticationFailed(_("MSG_MUST_INCLUDE_LOGIN_AND_PASSWORD"))
