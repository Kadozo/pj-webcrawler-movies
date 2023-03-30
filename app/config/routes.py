from fastapi import FastAPI, APIRouter, Request
from app.config.settings import getSettings
from starlette import status

from app.models.watchable import routes as watchable_routes
from app.models.genre import routes as genre_routes
from crawler.Crawler import Crawler
from .service import ServiceManager


router = APIRouter(prefix="/crawler")

@router.get(
    "/run",
    description="to execute the crawler script",
    status_code=status.HTTP_200_OK
)
async def get(req: Request):
    response = await ServiceManager(req).run()
    return {"response": response == 0, "quantity": response}

settings = getSettings()

def init_routes(app: FastAPI):
    app.include_router(router)
    app.include_router(genre_routes.router)
    app.include_router(watchable_routes.router)