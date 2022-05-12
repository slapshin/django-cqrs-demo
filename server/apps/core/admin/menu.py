from jnt_admin_tools.menu import Menu, items, reverse


class AdminMenu(Menu):
    """Main admin menu."""

    def __init__(self, **kwargs):
        """Initializing."""
        super().__init__(**kwargs)

        self.children += [
            items.MenuItem("Home", reverse("admin:index")),
            items.AppList(title="Applications"),
        ]
