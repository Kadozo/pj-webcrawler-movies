from fastapi import Request, HTTPException
from tortoise.exceptions import IntegrityError, DoesNotExist, OperationalError
from app.models.genre.model import Genre
from app.models.genre.repository import GenreRepository

class CreateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = GenreRepository()
    
    def __validate_types(self, data: dict) -> None:
        if data.get('name', None) is None:
            raise HTTPException(status_code=400, detail="Name parameter is required")

    def __validate(self, data: dict) -> None:
        self.__validate_types(data)

    async def create(self, model: dict) -> Genre:
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
        self.__repository = GenreRepository()
    
    def __validate_types(self, id: int) -> bool:
        if id is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    
    def __validate(self, id: int) -> bool:
        return self.__validate_types(id)
    
    async def get(self, id: int) -> Genre:
        if self.__validate(id):
            try:
                return await self.__repository.get_one(id)
            except DoesNotExist as e:
                raise HTTPException(status_code=404, detail="Genre does not exist.")
            except OperationalError as e:
                raise HTTPException(status_code=500, detail="error ocurred in query SQL.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Unknow error ocurred.")


class GetByNameService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = GenreRepository()
    
    def __validate_types(self, name: str) -> bool:
        if name is not None:
            return True
        raise HTTPException(status_code=422, detail="Parameters passeds not valid. ")
    
    def __validate(self, name: str) -> bool:
        return self.__validate_types(name)

    async def get(self, name: str) -> Genre:
        if self.__validate(name):
            try:
                result =  await self.__repository.execute_sql(f"select * from genre where name='{name}'")
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
        self.__repository = GenreRepository()
        self.__get_service = GetByIdService(req)
    
    def __validate_types(self, data: dict) -> None:
        if data.get('name', None) is None:
            raise HTTPException(status_code=400, detail="Name parameter is required")

    async def __validate(self, id: int, data: dict) -> Genre:
        self.__validate_types(data)
        return await self.__get_service.get(id)

    async def update(self, id: int, data: dict) -> Genre:
        model = await self.__validate(id, data)
        try:
            model.name = data.get('name')
            return await self.__repository.update(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unknown error ocurred")