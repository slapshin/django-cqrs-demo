from apps.blogs.logic.queries import posts

QUERIES = (
    (posts.list.Query, posts.list.QueryHandler),
    (posts.retrieve.Query, posts.retrieve.QueryHandler),
    (posts.my.Query, posts.my.QueryHandler),
)
