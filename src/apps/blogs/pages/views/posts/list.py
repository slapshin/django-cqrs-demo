from django.http import HttpRequest

from apps.blogs.logic.queries import posts
from apps.core.pages.base_list_query import BaseListQueryView


class View(BaseListQueryView):
    """Posts list view."""

    query = posts.list.Query
    template_name = "posts/list.html"

    def create_query(self, request: HttpRequest) -> posts.list.Query:
        """Create query to execute."""
        return self.query()
