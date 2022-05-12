from django.contrib.auth import get_user_model


def test_create_superuser(db):
    """Test that superuser is created with proper flags."""
    su = get_user_model().objects.create_superuser("foo", "bar")

    assert su.login == "foo"
    assert su.password != "bar"  # should be hashed
    assert su.is_staff
    assert su.is_superuser


def test_create_user(db):
    """Test that user is created with proper flags."""
    user = get_user_model().objects.create_user("foo", "bar", is_staff=False)

    assert user.login == "foo"
    assert user.password != "bar"  # should be hashed
    assert not user.is_staff
    assert not user.is_superuser
