from fastapi import APIRouter, Request
from starlette import status
import app.models.genre.services as services

router = APIRouter(prefix="/genre")

@router.get(
    "/movies",
    description="Get all genres in repository with average rating_imdb based on movies",
    status_code=status.HTTP_200_OK
)
async def get_genres_avg_movie(req: Request):
    result = await services.GetAvg(req).get(type="movies")
    return {"genres": result}

@router.get(
    "/movies/{name}",
    description="Get a genre in repository with average rating_imdb based on movies",
    status_code=status.HTTP_200_OK
)
async def get_genre_avg_movie_by_name(name: str, req: Request):
    result = await services.GetAvg(req).get(type="movies", name=name)
    return {"genres": result}

@router.get(
    "/series",
    description="Get all genres in repository with average rating_imdb based on series",
    status_code=status.HTTP_200_OK
)
async def get_genre_avg_serie(req: Request):
    result = await services.GetAvg(req).get(type="series")
    return {"genres": result}

@router.get(
    "/series/{name}",
    description="Get a genre in repository with average rating_imdb based on series",
    status_code=status.HTTP_200_OK
)
async def get_genre_avg_serie_by_name(name: str, req: Request):
    result = await services.GetAvg(req).get(type="series", name=name)
    return {"genres": result}

@router.get(
    "/avg",
    description="Get all genres in repository with average rating_imdb",
    status_code=status.HTTP_200_OK
)
async def get_genre_avg(req: Request):
    result = await services.GetAvg(req).get()
    return {"genres": result}

@router.get(
    "/",
    description="Get all genres in repository",
    status_code=status.HTTP_200_OK
)
async def get_genre(req: Request):
    result = await services.GetAll(req).get()
    return {"genres": result}