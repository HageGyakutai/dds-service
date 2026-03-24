from importlib.util import find_spec
from config.settings.components.security import DEBUG

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "apps.transactions",
    "apps.references",
]


if DEBUG and find_spec("debug_toolbar") is not None:
    INSTALLED_APPS.append("debug_toolbar")
