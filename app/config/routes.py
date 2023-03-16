from fastapi import FastAPI
from app.config.settings import getSettings

from app.models.watchable.routes import router as routerWatchable
from app.models.genre.routes import router as routerGenre

settings = getSettings()

def init_routes(app: FastAPI):
    app.include_router(routerGenre)
    app.include_router(routerWatchable)