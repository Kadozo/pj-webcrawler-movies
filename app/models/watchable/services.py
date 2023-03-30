from fastapi import Request
from app.models.watchable.model import Watchable
from app.models.watchable.repository import WatchableRepository

class WatchableService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableRepository()
    
    async def create(self, watchable: dict) -> Watchable:
        try:
            return await self.__repository.create(watchable)
        except Exception as e:
            raise e
        
    async def get_by_title(self, title: str) -> Watchable:
        try:
            watchable = await self.__repository.execute_sql(f"select * from watchable where title='{title}'")
            if len(watchable) > 0:
                return watchable[0]
            else:
                return None
        except Exception as e:
            raise e
    
    async def get_by_id(self, id: int) -> Watchable:
        try:
            watchable = await self.__repository.get_one(id)
            return watchable
        except Exception as e:
            raise e

    async def update(self, id: int, data: dict) -> Watchable:
        try:
            watchable = await self.get_by_id(id)
            
            watchable.title = data.get('title')
            watchable.age = data.get('age')
            watchable.start_year = data.get('start_year')
            watchable.end_year = data.get('end_year')
            watchable.imdb_rating = data.get('imdb_rating')
            watchable.tomatoes_rating = data.get('tomatoes_rating')
            watchable.ranking = data.get('ranking')
            watchable.runtime = data.get('runtime')
            watchable.type = data.get('type')
            watchable.metascore_rating = data.get('metascore_rating')

            result = await self.__repository.update(watchable)
            return result
        except Exception as e:
            raise e