import os

DEBUG = os.getenv("DEBUG") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = [h.strip() for h in os.getenv("HOSTS", "").split(",") if h.strip()]
