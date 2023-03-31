from fastapi import Request
from app.models.genre.model import Genre
from app.models.genre.repository import GenreRepository
class GenreService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = GenreRepository()
    
    async def create(self, genre: dict) -> Genre:
        try:
            return await self.__repository.create(genre)
        except Exception as e:
            raise e
        
    async def get_by_name(self, name: str) -> Genre:
        try:
            genre = await self.__repository.execute_sql(f"select * from genre where name='{name}'")
            if len(genre) > 0:
                return genre[0]
            else:
                return None
        except Exception as e:
            raise e
    
    async def get_by_id(self, id: int) -> Genre:
        try:
            genre = await self.__repository.get_one(id)
            return genre
        except Exception as e:
            raise e

    async def update(self, id: int, data: dict) -> Genre:
        try:
            genre = await self.get_by_id(id)
            #faz o update
            result = await self.__repository.update(genre)
            return result
        except Exception as e:
            raise e