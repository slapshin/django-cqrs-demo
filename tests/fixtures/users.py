import pytest

DEFAULT_USERNAME = "user"
DEFAULT_USER_PASSWORD = "password"  # noqa: S105


@pytest.fixture()
def user(db, django_user_model, django_username_field):
    """A Django user.

    This uses an existing user with username "user", or creates a new one with
    password "password".
    """
    username_field = django_username_field

    try:
        return django_user_model.objects.get(
            **{username_field: DEFAULT_USERNAME},
        )
    except django_user_model.DoesNotExist:
        return django_user_model.objects.create_user(
            DEFAULT_USERNAME,
            DEFAULT_USER_PASSWORD,
        )


@pytest.fixture()
def superuser(db, django_user_model, django_username_field):
    """A Django user.

    This uses an existing user with username "user", or creates a new one with
    password "password".
    """
    username_field = django_username_field

    try:
        new_user = django_user_model.objects.get(
            **{username_field: DEFAULT_USERNAME},
        )
    except django_user_model.DoesNotExist:
        return django_user_model.objects.create_superuser(
            DEFAULT_USERNAME,
            DEFAULT_USER_PASSWORD,
        )

    new_user.is_superuser = True
    new_user.is_staff = True
    new_user.save()
    return new_user
