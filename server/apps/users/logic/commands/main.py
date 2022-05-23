from apps.users.logic.commands import (
    login,
    logout,
    register,
    send_registration_notification,
)

COMMANDS = (
    (register.Command, register.CommandHandler),
    (login.Command, login.CommandHandler),
    (logout.Command, logout.CommandHandler),
    (logout.Command, logout.CommandHandler),
    (
        send_registration_notification.Command,
        send_registration_notification.CommandHandler,
    ),
)
