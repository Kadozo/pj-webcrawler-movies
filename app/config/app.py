from fastapi import FastAPI
from app.config.settings import getSettings

settings = getSettings()

"""Creating App"""
def get_app():
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
    )
    return app