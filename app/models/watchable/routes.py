from fastapi import APIRouter, Request
from app.models.watchable import schema
from app.models.watchable.repository import WatchableRepository
from starlette import status

router = APIRouter()

@router.get(
    "/{id}",
    description="Router to get all measurements ordering",
    status_code=status.HTTP_200_OK
)
async def get_measurement(req: Request, id: str):
    return {"measurements": req.query_params, "id": id}