import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    login = factory.Sequence(lambda index: "User {0}".format(index))
    email = factory.Sequence(lambda index: "user_{0}@gl.com".format(index))
    name = factory.Faker("name")
    is_staff = False
    is_active = True

    class Meta:
        model = User
