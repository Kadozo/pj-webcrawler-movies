from fastapi import APIRouter
from fastapi.params import Query
from starlette import status
import app.models.watchable.services as services

router = APIRouter(prefix="/watchable")

@router.get(
    "",
    description="Route that captures all watchables from the database, based on type (type), title (title), unique identifier (id) and/or genres (genre).",
    status_code=status.HTTP_200_OK
)
async def get_watchable(type: str = Query(None), title: str = Query(None), id: str = Query(None), genres: list[str] = Query(None)):

    result = await services.GetService(type=type, title=title, id=id, genre=genres).run()
    return {"watchables": result}