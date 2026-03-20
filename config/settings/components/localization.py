import os

from django.utils.translation import gettext_lazy as _

from config.settings.base import BASE_DIR

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "")

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
