from apps.users.logic.commands import register, login, logout

COMMANDS = (
    (register.Command, register.CommandHandler),
    (login.Command, login.CommandHandler),
    (logout.Command, logout.CommandHandler),
)
