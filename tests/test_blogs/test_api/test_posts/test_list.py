from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from apps.blogs.models import Post
from tests.test_blogs.factories.post import PostFactory
from tests.test_users.factories.user import UserFactory


@pytest.fixture()
def posts(db):
    """Posts to test."""
    return PostFactory.create_batch(3)


def test_success(api_client: APIClient, posts: list[Post]):
    """Test success posts list."""
    response = api_client.get("/api/posts")

    assert response.status_code == HTTPStatus.OK
    assert len(response.data) == 3


def test_author(api_client: APIClient, posts: list[Post]):
    """Test success posts list."""
    author = UserFactory.create()
    PostFactory.create_batch(2, author=author)
    response = api_client.get(
        "/api/posts",
        {
            "author": author.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.data) == 2
