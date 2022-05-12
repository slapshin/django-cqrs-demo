from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    USERNAME_FIELD = "email"  # noqa: WPS115

    email = models.EmailField(
        max_length=50,  # noqa:  WPS432
        unique=True,
        verbose_name=_("VN__EMAIL"),
        help_text=_("HT__EMAIL"),
    )

    is_staff = models.BooleanField(
        default=True,
        verbose_name=_("VN__IS_STAFF"),
        help_text=_("HT__IS_STAFF"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("VN__IS_ACTIVE"),
        help_text=_("HT__IS_ACTIVE"),
    )

    objects = UserManager()  # noqa: WPS110

    class Meta:
        verbose_name = _("VN__USER")
        verbose_name_plural = _("VN__USERS")

    def __str__(self):
        """Text representation."""
        return self.email

    def get_short_name(self):
        """Get user short name."""
        return self.email
