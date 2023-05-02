#!/usr/bin/env python


import os
import sys
from pathlib import PurePath

BASE_DIR = PurePath(__file__).parent


def _check_django_installed() -> None:
    try:
        import django  # noqa: F401, WPS433
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            + "available on your PYTHONPATH environment variable? Did you "
            + "forget to activate a virtual environment?",
        )


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import (  # noqa: WPS433
            execute_from_command_line,
        )
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        _check_django_installed()

        raise
    execute_from_command_line(sys.argv)
