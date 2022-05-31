import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client() -> APIClient:
    """API client."""
    return APIClient()
