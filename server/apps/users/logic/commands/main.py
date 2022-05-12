from apps.users.logic.commands import login, logout, register

COMMANDS = (
    (register.Command, register.CommandHandler),
    (login.Command, login.CommandHandler),
    (logout.Command, logout.CommandHandler),
)
