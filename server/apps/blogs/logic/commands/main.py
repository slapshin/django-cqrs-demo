from apps.blogs.logic.commands import posts

COMMANDS = (
    (posts.create.Command, posts.create.CommandHandler),
    (posts.update.Command, posts.update.CommandHandler),
    (posts.delete.Command, posts.delete.CommandHandler),
)
