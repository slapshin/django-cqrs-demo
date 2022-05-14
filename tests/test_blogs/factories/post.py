import factory

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus


class PostFactory(factory.django.DjangoModelFactory):
    """Post factory."""

    class Meta:
        model = Post

    title = factory.Faker("text", max_nb_chars=50)
    content = factory.Faker("text")  # noqa: WPS110
    status = PostStatus.PUBLISHED
