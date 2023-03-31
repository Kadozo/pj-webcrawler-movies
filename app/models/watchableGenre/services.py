from app.models.watchableGenre.model import WatchableGenre
from app.models.watchableGenre.repository import WatchableGenreRepository

from fastapi import Request


class WatchableGenreService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableGenreRepository()
    
    async def create(self, watchableGenre: dict) -> WatchableGenre:
        try:
            return await self.__repository.create(watchableGenre)
        except Exception as e:
            raise e
        
    async def get_by_watchable_id(self, watchableId: int) -> WatchableGenre:
        try:
            watchableGenre = await self.__repository.execute_sql(f"select * from watchablegenre where watchable_id='{watchableId}'")
            if len(watchableGenre) > 0:
                return watchableGenre[0]
            else:
                return None
        except Exception as e:
            raise e
    
    async def get_by_genre_id(self, genreId: int) -> WatchableGenre:
        try:
            watchableGenre = await self.__repository.execute_sql(f"select * from watchablegenre where genre_id='{genreId}'")
            if len(watchableGenre) > 0:
                return watchableGenre[0]
            else:
                return None
        except Exception as e:
            raise e
    
    async def get_by_id(self, id: int) -> WatchableGenre:
        try:
            watchable = await self.__repository.get_one(id)
            return watchable
        except Exception as e:
            raise e

    async def update(self, id: int, data: dict) -> WatchableGenre:
        try:
            watchableGenre = await self.get_by_id(id)
            #Faz o update
            result = await self.__repository.update(watchableGenre)
            return result
        except Exception as e:
            raise e