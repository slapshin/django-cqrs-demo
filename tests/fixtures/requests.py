import pytest

from tests.helpers.request_factory import RequestFactory


@pytest.fixture()
def rf() -> RequestFactory:
    """Provides request factory."""
    return RequestFactory()
