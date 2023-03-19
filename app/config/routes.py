from fastapi import FastAPI, APIRouter, Request
from app.config.settings import getSettings
from starlette import status

from app.models.watchable import routes as watchable_routes
from app.models.genre import routes as genre_routes

router = APIRouter(prefix="/crawler")

@router.get(
    "/exec",
    description="description",
    status_code=status.HTTP_200_OK
)
async def get(req: Request):
    return {"response": req.query_params}

settings = getSettings()

def init_routes(app: FastAPI):
    app.include_router(router)
    app.include_router(genre_routes.router)
    app.include_router(watchable_routes.router)