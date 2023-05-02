from apps.core.api.routers import ActionsRouter
from apps.users.api.views import login, logout, register

router = ActionsRouter()
router.post("login", login.View.as_view())
router.post("logout", logout.View.as_view())
router.post("register", register.View.as_view())
