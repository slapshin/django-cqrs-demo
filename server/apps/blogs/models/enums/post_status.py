from django.db import models
from django.utils.translation import gettext_lazy as _


class PostStatus(models.TextChoices):
    """Post status enum."""

    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")
