from django.http import HttpRequest

from apps.blogs.logic.queries import posts
from apps.core.logic import queries
from apps.core.pages.base_list_query import BaseListQueryView


class View(BaseListQueryView):
    """My posts view."""

    query = posts.my.Query
    template_name = "posts/list.html"

    def create_query(self, request: HttpRequest) -> queries.IQuery:
        """Create query to execute."""
        return self.query(
            user_id=request.user.id if request.user.is_authenticated else None,
        )
