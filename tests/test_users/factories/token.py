import string

import factory
from factory import fuzzy

from apps.users.models import Token
from tests.test_users.factories.user import UserFactory


class TokenFactory(factory.django.DjangoModelFactory):
    """Token factory."""

    key = fuzzy.FuzzyText(
        length=40, chars=string.ascii_uppercase + string.digits,
    )
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Token
