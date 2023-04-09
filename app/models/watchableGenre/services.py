from app.models.watchableGenre.model import WatchableGenre
from app.models.watchableGenre.repository import WatchableGenreRepository
from app.models.watchable.repository import WatchableRepository
from app.models.genre.repository import GenreRepository

from tortoise.exceptions import IntegrityError, OperationalError, DoesNotExist
from fastapi import Request, HTTPException


class CreateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableGenreRepository()
        self.__watchable_repository = WatchableRepository()
        self.__genre_repository = GenreRepository()
    
    async def __exists_watchable(self, watchable_id: str)-> bool:
        result = await self.__watchable_repository.get_one(watchable_id)
        return result is not None

    async def __exists_genre(self, genre_id: int) -> bool:
        result = await self.__genre_repository.get_one(genre_id)
        return result is not None
    
    def __validate_types(self, genre_id: int, watchable_id: str) -> bool:
        if genre_id is not None and watchable_id is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")

    async def __validate(self, genre_id: int, watchable_id: str) -> bool:
        self.__validate_types(genre_id, watchable_id)
        if await self.__exists_genre(genre_id):
            if await self.__exists_watchable(watchable_id):
                return True
            raise HTTPException(status_code=404, detail="Watchable not found.")
        raise HTTPException(status_code=404, detail="Genre not found.")

    async def create(self, model: dict) -> WatchableGenre:
        await self.__validate(model['genre_id'], model['watchable_id'])

        try:
            return await self.__repository.create(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error was ocurred while creating the watchable.")
            
class GetByLinkService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableGenreRepository()

    def __validate_types(self, genre_id: int, watchable_id: str) -> bool:
        if genre_id is not None and watchable_id is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    def __validate(self, genre_id: int, watchable_id: str) -> bool:
        return self.__validate_types(genre_id, watchable_id)
    
    async def get(self, genre_id: int, watchable_id: str) -> WatchableGenre:
        if self.__validate(genre_id, watchable_id):
            try:
                result = await self.__repository.execute_sql(f"select * from watchablegenre where watchable_id='{watchable_id}' and genre_id={genre_id}")
                if len(result) > 0:
                    return result[0]
                else:
                    return None
            except OperationalError as e:
                raise HTTPException(status_code=500, detail="error ocurred in query SQL.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Unknow error ocurred.")

class GetByIdService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableGenreRepository()

    def __validate_types(self, id: int) -> bool:
        if id is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    
    def __validate(self, id: int) -> bool:
        return self.__validate_types(id)
    
    async def get(self, id: int) -> WatchableGenre:
        if self.__validate(id):
            try:
                return await self.__repository.get_one(id)
            except DoesNotExist as e:
                raise HTTPException(status_code=404, detail="WatchableGenre does not exist.")
            except OperationalError as e:
                raise HTTPException(status_code=500, detail="error ocurred in query SQL.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Unknow error ocurred.")

class UpdateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableGenreRepository()
        self.__get_service = GetByIdService(req)

    async def __validate(self, id: int) -> WatchableGenre:
        return await self.__get_service.get(id)

    async def update(self, id: int, data: dict) -> WatchableGenre:
        model = await self.__validate(id)
        try:
            model.genre = data.get('genre_id')
            model.watchable = data.get('watchable_id')
            return await self.__repository.update(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unknown error ocurred")