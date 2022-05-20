import factory

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from tests.test_users.factories.user import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    """Post factory."""

    class Meta:
        model = Post

    title = factory.Faker("text", max_nb_chars=50)
    content = factory.Faker("text")  # noqa: WPS110
    status = PostStatus.PUBLISHED
    author = factory.SubFactory(UserFactory)
