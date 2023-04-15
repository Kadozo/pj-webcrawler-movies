from fastapi import Request, HTTPException
from tortoise.exceptions import IntegrityError, OperationalError
from app.models.genre.model import Genre
from app.models.genre.repository import GenreRepository
from tortoise import Tortoise

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


class UpdateService():
    def __init__(self, req: Request):
        self.__req = req
        self.__repository = GenreRepository()
    
    def __validate_types(self, data: dict) -> None:
        if data.get('name', None) is None:
            raise HTTPException(status_code=400, detail="Name parameter is required")

    async def __validate(self, id: int, data: dict) -> Genre:
        self.__validate_types(data)
        genre = await GetService(id=id).run()
        return genre

    async def update(self, id: int, data: dict) -> Genre:
        model = await self.__validate(id, data)
        try:
            model.name = data.get('name')
            return await self.__repository.update(model)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="Database integrity affected.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unknown error ocurred")

class GetAvgService():
    def __init__(self, w_type: str, g_name: str):
        self.__w_type = w_type.lower() if w_type else None
        self.__g_name = g_name.lower() if g_name else None
        self.__repository = Tortoise.get_connection('default')
    
    def __make_where(self):
        where = f"WHERE w.type='{self.__w_type}'" if self.__w_type else ""
        concatText = " AND " if where != "" else " WHERE "
        where += concatText + f"LOWER(g.name) LIKE '%{self.__g_name}%'" if self.__g_name else ""
        return where
    
    async def run(self) -> Genre:
        try:
            where = self.__make_where()
            query = f"""
                SELECT g.name AS name, ROUND(AVG(w.imdb_rating),3) AS imdb_avg,
                ROUND(AVG(w.metascore_rating),3) AS matescore_avg,
                ROUND(AVG(w.tomatoes_rating), 3) AS tomatoes_avg
                FROM watchable w JOIN watchablegenre w2 ON w.id=w2.watchable_id JOIN genre g ON g.id=w2.genre_id
                {where} GROUP BY g.name
                ORDER BY imdb_avg desc
            """
            return await self.__repository.execute_query_dict(query)
        except OperationalError as e:
            raise HTTPException(status_code=500, detail=f"error ocurred in query SQL: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unknown error ocurred: {str(e)}")

class GetService():
    def __init__(self, name: str, id: int):
        self.__id = id
        self.__name = name.lower() if name else None
        self.__repository = Tortoise.get_connection('default')

    def __make_where(self) -> str:
        where = f"WHERE id={self.__id}" if self.__id else ""
        concat = " OR " if where != "" else " WHERE "
        where += concat + f"LOWER(name) LIKE '%{self.__name}%'" if self.__name else ""
        return where
        
    async def run(self) -> list[Genre] | Genre:
        try:
            where = self.__make_where()
            result = await self.__repository.execute_query_dict(f"SELECT id, name FROM genre {where} ORDER BY name")
            if "OR" not in where and self.__id:
                result = result[0] if len(result) else None
            return result
        except OperationalError as e:
            raise HTTPException(status_code=500, detail=f"error ocurred in query SQL: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unknow error ocurred: {str(e)}")