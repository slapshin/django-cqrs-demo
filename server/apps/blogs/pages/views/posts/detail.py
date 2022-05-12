from django.http import HttpRequest

from apps.blogs.logic.queries import posts
from apps.core.logic import queries
from apps.core.pages.base_retrieve_query import BaseRetrieveQueryView


class View(BaseRetrieveQueryView):
    query = posts.retrieve.Query
    template_name = 'posts/detail.html'

    def get_query(self, request: HttpRequest) -> queries.IQuery:
        return self.query(
            user_id=request.user.id if request.user.is_authenticated else None,
            post_id=self.kwargs["id"],
        )
