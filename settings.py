import os

from dotenv import load_dotenv

load_dotenv('.env')

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL")
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "res.database.classes"],
            "default_connection": "default",
        }
    }
}
