# Import base settings
from backend.settings.base import *


# Set the debug status
DEBUG = True


# Database
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "delarship_database",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1",
        },
    }
}
