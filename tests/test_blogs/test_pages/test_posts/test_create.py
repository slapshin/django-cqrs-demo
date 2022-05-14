from http import HTTPStatus

from django.test import Client

from apps.blogs.models import Post
from apps.blogs.models.enums import PostStatus
from apps.users.models import User


def test_initial(client: Client, user: User):
    """Test initial page."""
    response = client.get("/posts/new/")

    assert response.status_code == HTTPStatus.OK


def test_success(client: Client, user: User):
    """Test success creation."""
    client.force_login(user)
    response = client.post(
        "/posts/new/",
        {
            "title": "post title",
            "content": "post content",
            "status": PostStatus.DRAFT,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    post = Post.objects.filter(title="post title").first()
    assert response.url == "/posts/{0}/".format(post.id)
    assert post.content == "post content"
    assert post.status == PostStatus.DRAFT
    assert post.author == user


def test_not_user(client: Client, user: User):
    """Test not auth user."""
    response = client.post(
        "/posts/new/",
        {
            "title": "post title",
            "content": "post content",
            "status": PostStatus.DRAFT,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/login/"
