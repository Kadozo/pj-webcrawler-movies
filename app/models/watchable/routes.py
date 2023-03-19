from fastapi import APIRouter, Request
from app.models.watchable import schema
from app.models.watchable.repository import WatchableRepository
from starlette import status

router = APIRouter(prefix="/watchable")

@router.get(
    "/",
    description="description",
    status_code=status.HTTP_200_OK
)
async def get(req: Request):
    return {"response": req.query_params}