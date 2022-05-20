from apps.blogs.api.serializers import PostSerializer
from apps.blogs.logic.queries import posts
from apps.core.api.views import BaseRetrieveQueryView
from apps.core.logic import queries


class View(BaseRetrieveQueryView):
    """Post retrieve view."""

    query = posts.retrieve.Query
    output_serializer = PostSerializer

    def create_query(self) -> queries.IQuery:
        """Create query to execute."""
        return self.query(
            post_id=self.kwargs["pk"],
            user_id=self.user.id if self.user else None,
        )
