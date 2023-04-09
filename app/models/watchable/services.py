from fastapi import Request, HTTPException
from app.models.watchable.model import Watchable
from app.models.watchable.repository import WatchableRepository
from tortoise.exceptions import IntegrityError, OperationalError, DoesNotExist

class CreateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableRepository()
    
    def __validate_types(self, data: dict) -> None:
        if data.get('id', None) is None:
            raise HTTPException(status_code=400, detail="Id parameter is required")
        if data.get('title', None) is None:
            raise HTTPException(status_code=400, detail="Title parameter is required")
        if data.get('type', None) is None:
            raise HTTPException(status_code=400, detail="Type parameter is required")

    def __validate(self, data: dict) -> None:
        self.__validate_types(data)

    async def create(self, model: dict) -> Watchable:
        self.__validate(model)

        try:
            return await self.__repository.create(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error was ocurred while creating the watchable.")

class GetByIdService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableRepository()
    
    def __validate_types(self, id: str) -> bool:
        if id is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    
    def __validate(self, id: str) -> bool:
        return self.__validate_types(id)
    
    async def get(self, id: str) -> Watchable:
        if self.__validate(id):
            try:
                return await self.__repository.get_one(id)
            except DoesNotExist as e:
                raise HTTPException(status_code=404, detail="Watchable does not exist.")
            except OperationalError as e:
                raise HTTPException(status_code=500, detail="error ocurred in query SQL.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Unknow error ocurred.")


class GetByTitleService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableRepository()
    
    def __validate_types(self, title: str) -> bool:
        if title is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    
    def __validate(self, title: str) -> bool:
        return self.__validate_types(title)

    async def get(self, title: str) -> Watchable:
        if self.__validate(title):
            try:
                result =  await self.__repository.execute_sql(f"select * from watchable where title='{title}'")
                if len(result) > 0:
                    return result[0]
                else:
                    return None
            except OperationalError as e:
                raise HTTPException(status_code=500, detail="error ocurred in query SQL.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Unknow error ocurred.")

class UpdateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = WatchableRepository()
        self.__get_service = GetByIdService(req)
    
    def __validate_types(self, data: dict) -> None:
        if data.get('id', None) is None:
            raise HTTPException(status_code=400, detail="Id parameter is required")
        if data.get('title', None) is None:
            raise HTTPException(status_code=400, detail="Title parameter is required")
        if data.get('type', None) is None:
            raise HTTPException(status_code=400, detail="Type parameter is required")

    async def __validate(self, id: str, data: dict) -> Watchable:
        self.__validate_types(data)
        return await self.__get_service.get(id)

    async def update(self, id: str, data: dict) -> Watchable:
        model = await self.__validate(id, data)
        try:
            model.title = data.get('title')
            model.age = data.get('age')
            model.start_year = data.get('start_year')
            model.end_year = data.get('end_year')
            model.imdb_rating = data.get('imdb_rating')
            model.tomatoes_rating = data.get('tomatoes_rating')
            model.last_ranking = model.ranking
            model.img = data.get('img')
            model.votes = data.get('votes')
            model.ranking = data.get('ranking')
            model.runtime = data.get('runtime')
            model.type = data.get('type')
            model.metascore_rating = data.get('metascore_rating')

            return await self.__repository.update(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unknown error ocurred")

