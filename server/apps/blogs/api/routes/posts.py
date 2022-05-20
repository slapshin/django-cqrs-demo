from apps.blogs.api.views import posts
from apps.core.api.routers import ActionsRouter

router = ActionsRouter()
router.get("posts", posts.list.View.as_view())
router.post("posts", posts.create.View.as_view())
router.get("posts/<int:pk>", posts.retrieve.View.as_view())
router.delete("posts/<int:pk>", posts.delete.View.as_view())
router.patch("posts/<int:pk>", posts.update.View.as_view())
