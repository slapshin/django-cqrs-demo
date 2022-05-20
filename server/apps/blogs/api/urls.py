from apps.blogs.api import routes

app_name = "api:blogs"

urlpatterns = routes.posts.router.urls
