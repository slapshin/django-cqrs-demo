from typing import Optional

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Users manager."""

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **kwargs,
    ):
        """Create user."""
        if not email:
            raise ValueError(_("VN__USER_MUST_HAVE_A_EMAIL"))

        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """Create superuser."""
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
