from fastapi import FastAPI, APIRouter, Request, HTTPException
from app.config.settings import getSettings
from starlette import status
from app.config import schema

from app.models.watchable import routes as watchable_routes
from app.models.genre import routes as genre_routes
from .services import ServiceManager


router = APIRouter()

@router.get(
    "/",
    description="Endpoint to welcome",
    status_code=status.HTTP_200_OK
)
def welcome():
    return {"message": "Welcome to Movies and Series Analysis API. To view the documentation for more information, visit '/docs' url."}

@router.post(
    "/crawler",
    description="to execute the crawler script",
    status_code=status.HTTP_200_OK
)
async def get(req: Request, params: schema.RunCrawler):
    await ServiceManager(req, params=params).run()
    return {"message": "crawler run successfully"}

settings = getSettings()

def init_routes(app: FastAPI):
    app.include_router(router)
    app.include_router(genre_routes.router)
    app.include_router(watchable_routes.router)