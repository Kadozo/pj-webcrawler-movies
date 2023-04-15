from app.models.genre import services as GenreServices
from app.models.watchableGenre import services as watchableGenreServices 
from app.models.watchable import services as WatchableServices

from crawler.Crawler import Crawler
from app.config import schema
from .settings import getSettings

from fastapi import Request, HTTPException

ROOT_FILE = "crawler/root.json"

class ServiceManager():
    def __init__(self, req: Request, params: schema.RunCrawler):
        self.__crawler = Crawler(offset=params.offset, site=params.site, limit=params.limit)
        self.__params = params
        self.__watchable_create = WatchableServices.CreateService(req)
        self.__watchable_update = WatchableServices.UpdateService(req)
        self.__watchable_get_by_id = WatchableServices.GetByIdService(req)
        self.__genre_create = GenreServices.CreateService(req)
        self.__watchable_genre_create = watchableGenreServices.CreateService(req)
        self.__watchable_genre_get_link = watchableGenreServices.GetByLinkService(req)
    
    async def run(self):
        self.__verify_entity()
        try:
            data = self.__crawler.run(ROOT_FILE)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str({"errors": e}))
        for array in data:
            errors = []
            for element in array:
                try:
                    await self.__save_element(element)
                except Exception as e:
                    errors.append(e)
            if len(errors) > 0:
                raise HTTPException(status_code=500, detail=str({"erros": errors}))

    async def __save_element(self, element: dict) -> None:
        watchable = await self.__watchable_get_by_id.get(element.get('id', None))
        if watchable is not None:
            watchable = await self.__watchable_update.update(id=watchable.id, data=element)
        else:
            watchable = await self.__watchable_create.create(element)
        for genre_name in element["genre"]:
            genre = await GenreServices.GetService(name=genre_name).run()
            genre = genre[0] if len(genre)>0 else None
            if genre is not None:
                link = await self.__watchable_genre_get_link.get(genre.id, watchable.id)
                if link is None:
                    await self.__watchable_genre_create.create({"watchable_id":watchable.id, "genre_id":genre.id})
            else:
                createdGenre = await self.__genre_create.create({"name":genre_name})
                await self.__watchable_genre_create.create({"watchable_id":watchable.id, "genre_id":createdGenre.id})
    
    def __verify_entity(self) -> None:
        settings = getSettings()
        if self.__params.user != settings.USER_ROOT or self.__params.password != settings.PASSWORD_ROOT:
            raise HTTPException(status_code=401, detail="Unauthorized user")