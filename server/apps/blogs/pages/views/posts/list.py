from django.http import HttpRequest

from apps.blogs.logic.queries import posts
from apps.core.logic import queries
from apps.core.pages.base_list_query import BaseListQueryView


class View(BaseListQueryView):
    query = posts.list.Query
    template_name = 'posts/list.html'

    def get_query(self, request: HttpRequest) -> queries.IQuery:
        return self.query()
