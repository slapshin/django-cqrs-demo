import string

import factory

from apps.users.models import Token
from tests.test_users.factories.user import UserFactory


class TokenFactory(factory.django.DjangoModelFactory):
    """Token factory."""

    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
    key = factory.fuzzy.FuzzyText(
        length=Token.key.max_length,
        chars=string.ascii_uppercase + string.digits,
    )
