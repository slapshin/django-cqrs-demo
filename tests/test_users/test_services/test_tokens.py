import pytest
from django.utils import timezone

from apps.users.models import Token
from apps.users.services.token import clear_tokens
from tests.test_users.factories.token import TokenFactory


def test_clear_token(settings, db):
    """Tokens should be deleted if they older than expire settings."""
    settings.REST_FRAMEWORK_TOKEN_EXPIRE = 1  # min
    tok = TokenFactory.create()
    Token.objects.filter(pk=tok.pk).update(
        created=timezone.now() - timezone.timedelta(minutes=10),
    )
    clear_tokens()

    with pytest.raises(Token.DoesNotExist):
        tok.refresh_from_db()


def test_clear_token_no_expire(settings, db):
    """No tokens should be deleted with disabled expire."""
    settings.REST_FRAMEWORK_TOKEN_EXPIRE = None
    tok = TokenFactory(created=timezone.now() - timezone.timedelta(minutes=2))

    clear_tokens()

    tok.refresh_from_db()
