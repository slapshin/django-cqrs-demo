import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    class Meta:
        model = User

    email = factory.Sequence(lambda index: "user_{0}@mail.com".format(index))
    name = factory.Faker("name")
    is_staff = False
    is_active = True
