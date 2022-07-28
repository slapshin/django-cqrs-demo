from apps.blogs.api.serializers import PostSerializer
from apps.blogs.domain.queries import posts
from apps.core.api.views import BaseRetrieveQueryView


class View(BaseRetrieveQueryView):
    """Post retrieve view."""

    query = posts.retrieve.Query
    output_serializer = PostSerializer

    def create_query(self) -> posts.retrieve.Query:
        """Create query to execute."""
        return self.query(
            post_id=self.kwargs["pk"],
            user_id=self.user.id if self.user else None,
        )
