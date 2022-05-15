import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    """API client."""
    return APIClient()
