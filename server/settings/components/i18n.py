from django.utils.translation import gettext_lazy as _

from server import BASE_DIR

USE_I18N = True
USE_L10N = True

USE_TZ = True

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("MESSAGE__ENGLISH")),
]

LOCALE_PATHS = [
    BASE_DIR.joinpath("locale"),
]
