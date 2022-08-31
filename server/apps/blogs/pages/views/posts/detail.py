from django.http import HttpRequest

from apps.blogs.logic.queries import posts
from apps.core.pages.base_retrieve_query import BaseRetrieveQueryView


class View(BaseRetrieveQueryView):
    """Post detail view."""

    query = posts.retrieve.Query
    template_name = "posts/detail.html"

    def create_query(self, request: HttpRequest) -> posts.retrieve.Query:
        """Create query to execute."""
        return self.query(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
        )
