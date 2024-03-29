# Import base settings
from backend.settings.base import *


# Set the debug status
DEBUG = False


# Set allowed hosts
ALLOWED_HOSTS = [".vercel.app"]


# Database
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "dealership_database",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": os.environ["MONGO_DB_URI"],
            "username": os.environ["MONGO_DB_USERNAME"],
            "password": os.environ["MONGO_DB_PASSWORD"],
        },
    }
}
