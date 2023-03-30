from fastapi import Request
from app.models.watchable.model import Watchable
from app.models.watchable.services import WatchableService
from crawler.Crawler import Crawler

OFFSET = 250
SITE = "imdb"
LIMIT = 2500
ROOT_FILE = "crawler/root.json"

class ServiceManager():
    def __init__(self, req: Request):
        self.__crawler = Crawler(offset=OFFSET, site=SITE, limit=LIMIT)
        self.__req = req
        self.__watchable_service = WatchableService(req)
    
    async def run(self):
        data = self.__crawler.run(ROOT_FILE)
        error = 0
        for array in data:
            for element in array:
                if not await self.__save_element(element):
                    error += 1
                    print("An error occurred")
        return error

    async def __save_element(self, element: dict) -> bool:
        try:
            watchable = await self.__exists_element(element['title'])
            if watchable is not None:
                await self.__update_element(watchable, element)
            else:
                await self.__watchable_service.create(element)
            return True
        except Exception as e:
            print(e)
            return False
    
    async def __exists_element(self, title: str) -> Watchable:
        try:
            element = await self.__watchable_service.get_by_title(title)
            return element
        except Exception as e:
            raise e
    
    async def __update_element(self, watchable: Watchable, data: dict) -> Watchable:
        try:
            element = await self.__watchable_service.update(id=watchable.id, data=data)
            return element
        except Exception as e:
            raise e