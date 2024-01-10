# Import base settings
from backend.settings.base import *


# Set the debug status
DEBUG = False


# Database
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "Los-Santos-Customs",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": os.environ["MONGO_DB_URI"],
            "username": os.environ["MONGO_DB_USERNAME"],
            "password": os.environ["MONGO_DB_PASSWORD"],
        },
    }
}
