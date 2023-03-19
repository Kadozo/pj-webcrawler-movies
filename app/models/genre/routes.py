from fastapi import APIRouter
from app.models.genre import schema
from app.models.genre.repository import GenreRepository
from starlette import status

router = APIRouter(prefix="/genre")