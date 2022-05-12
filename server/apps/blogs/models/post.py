from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.blogs.models.enums import PostStatus


class Post(models.Model):
    """Post model."""

    title = models.CharField(
        max_length=255,  # noqa:  WPS432
        verbose_name=_("VN__TITLE"),
        help_text=_("HT__TITLE"),
    )

    content = models.TextField(
        verbose_name=_("VN__CONTENT"),
        help_text=_("HT__CONTENT"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("VN__CREATED_AT"),
        help_text=_("HT__CREATED_AT"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("VN__UPDATED_AT"),
        help_text=_("HT__UPDATED_AT"),
    )

    status = models.CharField(
        max_length=10,
        choices=PostStatus.choices,
        verbose_name=_("VN__STATUS"),
        help_text=_("HT__STATUS"),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_("VN__AUTHOR"),
        help_text=_("HT__AUTHOR"),
    )

    class Meta:
        verbose_name = _("VN__POST")
        verbose_name_plural = _("VN__POSTS")
        unique_together = ("author", "title")

    def __str__(self):
        """Text representation."""
        return self.title
