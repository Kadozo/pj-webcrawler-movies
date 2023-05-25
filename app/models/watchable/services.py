from fastapi import Request, HTTPException
from app.models.watchable.model import Watchable
from app.models.watchable.repository import WatchableRepository
from tortoise.exceptions import IntegrityError, OperationalError, DoesNotExist
from tortoise import Tortoise

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
            raise HTTPException(status_code=409, detail=f"Database integrity affected. {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error was ocurred while creating the watchable. {str(e)}")

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
                raise HTTPException(status_code=404, detail=f"Watchable does not exist. {str(e)}")
            except OperationalError as e:
                raise HTTPException(status_code=500, detail=f"error ocurred in query SQL. {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unknow error ocurred. {str(e)}")


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
            raise HTTPException(status_code=409, detail=f"Database integrity affected. {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unknown error ocurred. {str(e)}")

class GetService():
    def __init__(self, type: str, id: str, title: str, genre: list[str], limit: int, offset: int, only_img: bool):
        self.__type = type.lower() if type else None
        self.__title = title.lower() if title else None
        self.__id = id.lower() if id else None
        self.__genre = genre
        self.__limit = limit
        self.__offset = offset
        self.__only_img = only_img
        self.__repository = Tortoise.get_connection('default')
    
    def __validate_param(self, param: str | list[str], _type: str) -> None:
        if param is not None:
            if type(param) != str:
                if type(param) != list:
                    raise HTTPException(status_code=422, detail=f"Parameter {_type} not valid. ")
            elif len(param) > 100:
                raise HTTPException(status_code=422, detail=f"Parameter {_type} not valid. ")
    
    def __validate(self) -> None:
        self.__validate_param(self.__title, _type="title")
        self.__validate_param(self.__type, _type="type")
        self.__validate_param(self.__id, _type="id")
        self.__validate_param(self.__genre, _type="genre")

    def __make_text_where(self) -> str:
        where = ""
        if self.__id is not None:
            return f" WHERE w.id = '{self.__id}'"
        if self.__title is not None:
                where += f" WHERE LOWER(w.title) LIKE '%{self.__title}%'"
        if self.__type is not None:
            if where == "":
                where += f" WHERE w.type = '{self.__type}'"
            else:
                where += f" AND w.type = '{self.__type}'"
        return where

    def __make_text_having(self) -> str:
        having = ""
        if self.__genre is not None and len(self.__genre) > 0:
            having = "HAVING"
            for name in self.__genre:
                having += f" CONCAT(',', LOWER(genres), ',') LIKE '%,{name.lower()},%' AND"
            having = having.rstrip("AND")
        return having
    
    def __make_text_offset(self) -> str:
        offset = ""
        if self.__offset is not None:
            offset = f"OFFSET {self.__offset}"
        return offset
    
    def __make_text_limit(self) -> str:
        limit = ""
        if self.__limit is not None:
            limit = f"LIMIT {self.__limit}"
        return limit
    
    def __make_text_select(self) -> str:
        select = ""
        if self.__only_img:
            select = "w.img"
        else:
            select = "w.*, GROUP_CONCAT(g.name SEPARATOR ',') AS genres"
        return select

    async def run(self) -> Watchable:
        self.__validate()
        try:
            textWhere = self.__make_text_where()
            textHaving = self.__make_text_having()
            textLimit = self.__make_text_limit()
            textOffset = self.__make_text_offset()
            textSelect = self.__make_text_select()
            query = f"""
                SELECT {textSelect}
                FROM watchable w JOIN watchablegenre wg ON w.id = wg.watchable_id
                JOIN genre g ON g.id = wg.genre_id {textWhere}
                GROUP BY w.id {textHaving}
                ORDER BY CAST(REPLACE(ranking, ',', "") AS UNSIGNED) ASC
                {textLimit}
                {textOffset}
            """
            result = await self.__repository.execute_query_dict(query)
            if not self.__only_img:
                for watchable in result:
                    watchable['genres'] = watchable['genres'].split(',')
            return result
        except OperationalError as e:
            raise HTTPException(status_code=500, detail=f"error ocurred in query SQL: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unknow error ocurred: {str(e)}")