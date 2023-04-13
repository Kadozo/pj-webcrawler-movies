from fastapi import APIRouter, Request
from starlette import status
import app.models.watchable.services as services

router = APIRouter(prefix="/watchable")

@router.get(
    "/series",
    description="Get all series in repository",
    status_code=status.HTTP_200_OK
)
async def get_all_series(req: Request):
    result = await services.GetAllService(req).get(type="series")
    return {"series": result}

@router.get(
    "/series/{title}",
    description="Get a serie in repository with title informed",
    status_code=status.HTTP_200_OK
)
async def get_serie_by_title(title: str,req: Request):
    result = await services.GetByTitleService(req).get(title, "series")
    return {"series": result}

@router.get(
    "/movies",
    description="Get all movies in repository",
    status_code=status.HTTP_200_OK
)
async def get_all_movies(req: Request):
    result = await services.GetAllService(req).get(type="movies")
    return {"movies": result}

@router.get(
    "/{id}",
    description="Get a watchable in repository with id informed",
    status_code=status.HTTP_200_OK
)
async def get_by_id(id: str,req: Request):
    result = await services.GetByIdService(req).get(id)
    return {"movie": result}

@router.get(
    "/movies/{title}",
    description="Get a movie in repository with title informed",
    status_code=status.HTTP_200_OK
)
async def get_movie_by_title(title:str, req: Request):
    result = await services.GetByTitleService(req).get(title, "movies")
    return {"movies": result}

@router.get(
    "/genre-movie/{name}",
    description="Get a movie in repository with title informed",
    status_code=status.HTTP_200_OK
)
async def get_movie_by_title(name:str, req: Request):
    result = await services.GetByGenreService(req).get(type="movies", name=name)
    return {"movies": result}

@router.get(
    "/genre-serie/{name}",
    description="Get a movie in repository with title informed",
    status_code=status.HTTP_200_OK
)
async def get_movie_by_title(name:str, req: Request):
    result = await services.GetByGenreService(req).get(type="movies", name=name)
    return {"series": result}