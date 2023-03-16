from app.config.settings import getSettings
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

settings = getSettings()

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": settings.MODELS,
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI):
    register_tortoise(
        app=app,
        db_url=settings.DB_URL,
        generate_schemas=settings.GENERATE_SCHEMAS,
        modules={"models": settings.MODELS},
        add_exception_handlers=True,
    )