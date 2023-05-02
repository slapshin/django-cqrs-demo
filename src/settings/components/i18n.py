from django.utils.translation import gettext_lazy as _

USE_I18N = True

USE_TZ = True

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("MESSAGE__ENGLISH")),
]

LOCALE_PATHS = ["src/locale"]
