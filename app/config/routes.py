from fastapi import FastAPI
from app.config.settings import getSettings

from app.models.watchable import routes as watchable_routes
from app.models.genre import routes as genre_routes

settings = getSettings()

def init_routes(app: FastAPI):
    app.include_router(genre_routes.router, prefix="/genre")
    app.include_router(watchable_routes.router, prefix="/watchable")