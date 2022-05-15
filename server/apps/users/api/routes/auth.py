from apps.core.api.routers import ActionsRouter
from apps.users.api.views import login

router = ActionsRouter()
router.post("login", login.View.as_view())
