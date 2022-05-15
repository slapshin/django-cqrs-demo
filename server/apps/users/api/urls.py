from apps.users.api import routes

app_name = "api:users"

urlpatterns = routes.auth.router.urls
