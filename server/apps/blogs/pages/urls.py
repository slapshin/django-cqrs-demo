from django.urls import path

from apps.blogs.pages.views import posts

app_name = "blogs"

urlpatterns = [
    path("", posts.list.View.as_view(), name="home"),
    path("posts/my/", posts.my.View.as_view(), name="posts_my"),
    path("posts/new/", posts.create.View.as_view(), name="post_create"),
    path("posts/<int:id>/", posts.detail.View.as_view(), name="post_detail"),
    path("posts/<int:id>/edit/", posts.edit.View.as_view(), name="post_edit"),
    path(
        "posts/<int:id>/delete/",
        posts.delete.View.as_view(),
        name="post_delete",
    ),
]
