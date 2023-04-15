from fastapi import APIRouter, Request
from starlette import status
from fastapi.params import Query
import app.models.genre.services as services

router = APIRouter(prefix="/genre")

@router.get(
    "",
    description="Get genres by name or id",
    status_code=status.HTTP_200_OK
)
async def get_genre(id: int = Query(None), name: str = Query(None)):
    result = await services.GetService(id=id, name=name).run()
    return {"genres" if type(result) == list else "genre": result}

@router.get(
    "/scores",
    description="Get genres, averaging IMDb, Metascore, and Tomatoes scores, by name and/or whatchable type",
    status_code=status.HTTP_200_OK
)
async def get_scores(w_type: str = Query(None), g_name: str = Query(None)):
    result = await services.GetAvgService(w_type=w_type, g_name=g_name).run()
    return {"genres": result}