from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.watchableGenre.model import WatchableGenre

class WatchableGenreRepository:
    def __init__(self):
        self._entity = WatchableGenre
        self._model_creator = pydantic_model_creator(WatchableGenre)

    """
        Transform a watchableGenre object in a dictionary

        params:
            watchableGenre -> the watchableGenre object
        return:
            dictionary with the attributes of the watchableGenre object passed
    """
    async def to_dict(self, watchableGenre: WatchableGenre) -> dict:
        result = await self._model_creator.from_tortoise_orm(watchableGenre)
        return result.dict()

    """
        Create a new WatchableGenre

        params:
            watchableGenre dict with the type and value of the watchableGenre
        return:
            Object WatchableGenre -> if success
            None -> if failure
    """
    async def create(self, watchableGenre: dict) -> WatchableGenre:
        return await self._entity.create(**watchableGenre)
    

    """
        Update a WatchableGenre

        params:
            watchableGenre -> the watchableGenre to update
            data -> a dictionary with the new data to update
        return:
            O watchableGenre atualizado
        raises:
            ConfigurationError -> Configuration error
            ValueError -> When a passed parameter is not type compatible.
    """
    async def update(self, watchableGenre: WatchableGenre, data: dict) -> WatchableGenre:
        result = await watchableGenre.update_from_dict(data)
        return result

    """
        Get one watchableGenre where it has the same id as given.

        params:
            id of the watchableGenre wanted
        return:
            Object WatchableGenre found or None if not found
    """
    async def get_one(self, id: int) -> WatchableGenre:
        result = await self._entity.get_or_none(id=id)
        return result
    
    """
        Get all watchableGenres in the table

        return:
            list
    """
    async def get_all(self) -> list[WatchableGenre]:
        result = await self._entity.all()
        return result
    
    """
        Get one or more watchableGenre in the table accordingly to key and value provided.

        params:
            key -> the key that will be searched in the table
            value -> the value that will be searched in the table
        return:
            list
    """
    async def get_many(self, key: str, value: any) -> list[WatchableGenre]:
        result = await self._entity.filter(**{key:value})
        return result

    """
        Delete one watchableGenre in the table accordingly to the id provided.

        params:
            id -> the id of the watchableGenre to be deleted
        return
            True -> if success
            False -> if failure
    """
    async def delete(self, watchableGenre: WatchableGenre) -> bool:
        await watchableGenre.delete()
        return True

    """
        Execute a query in the data base freely

        params:
            query -> query string that will be executed in the data base
        return:
            Depends of the query string provided
    """
    async def execute_sql(self, query: str) -> any:
        return await self._entity.raw(query)