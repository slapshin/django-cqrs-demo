from django.urls import path

from apps.users.pages.views import users

app_name = "users"

urlpatterns = [
    path("registration", users.register.View.as_view(), name="register"),
    path("login", users.login.View.as_view(), name="login"),
    path("logout", users.logout.View.as_view(), name="logout"),
]
