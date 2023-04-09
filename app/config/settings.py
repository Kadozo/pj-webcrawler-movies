from decouple import config
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_VERSION: str = config("APP_VERSION", default="1")
    USER_ROOT: str = config("USER_ROOT")
    PASSWORD_ROOT: str = config("PASSWORD_ROOT")
    APP_DESCRIPTION: str = config("APP_DESCRIPTION", default="API")
    APP_NAME: str = config("APP_NAME", default="API")
    APP_PORT: int = config("APP_PORT", default=3333, cast=int)
    DB_URL = config("DB_URL")
    ORIGINS: list = [
        "http://localhost:3000",
        "https://localhost:3000"
    ]
    GENERATE_SCHEMAS: bool = config("GENERATE_SCHEMAS", default=False)
    MODELS: list = [
        "app.models.genre.model",
        "app.models.watchable.model",
        "app.models.watchableGenre.model",
        "aerich.models"
    ]



@lru_cache
def getSettings():
    return Settings()