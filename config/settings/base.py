from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"
