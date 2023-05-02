import pytest


@pytest.fixture(autouse=True)
def _django_settings(settings, tmpdir_factory) -> None:
    """Forces django test settings."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]
    settings.STORAGES["staticfiles"] = {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
