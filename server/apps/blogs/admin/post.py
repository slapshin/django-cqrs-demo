from django.contrib import admin

from apps.blogs.models.post import Post
from apps.core.admin.base import BaseModelAdmin


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    """Post admin."""
    list_display = (
        "title",
        "author",
        "status",
    )
    list_filter = ("author", "status")
    autocomplete_fields = ("author",)
    fields = (
        "author",
        "status",
        "title",
        "content",
        "created_at",
        "updated_at",
    )
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
