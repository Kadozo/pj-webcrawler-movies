from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.watchable.model import Watchable

class WatchableRepository:
    def __init__(self):
        self._entity = Watchable
        self._model_creator = pydantic_model_creator(Watchable)

    """
        Transform a watchable object in a dictionary

        params:
            watchable -> the watchable object
        return:
            dictionary with the attributes of the watchable object passed
    """
    async def to_dict(self, watchable: Watchable) -> dict:
        result = await self._model_creator.from_tortoise_orm(watchable)
        return result.dict()

    """
        Create a new Watchable

        params:
            watchable dict with the type and value of the watchable
        return:
            Object Watchable -> if success
            None -> if failure
    """
    async def create(self, watchable: dict) -> Watchable:
        return await self._entity.create(**watchable)
    

    """
        Update a Watchable

        params:
            watchable -> the watchable to update
            data -> a dictionary with the new data to update
        return:
            O watchable atualizado
        raises:
            ConfigurationError -> Configuration error
            ValueError -> When a passed parameter is not type compatible.
    """
    async def update(self, watchable: Watchable, data: dict) -> Watchable:
        result = await watchable.update_from_dict(data)
        return result

    """
        Get one watchable where it has the same id as given.

        params:
            id of the watchable wanted
        return:
            Object Watchable found or None if not found
    """
    async def get_one(self, id: int) -> Watchable:
        result = await self._entity.get_or_none(id=id)
        return result
    
    """
        Get all watchables in the table

        return:
            list
    """
    async def get_all(self) -> list[Watchable]:
        result = await self._entity.all()
        return result
    
    """
        Get one or more watchable in the table accordingly to key and value provided.

        params:
            key -> the key that will be searched in the table
            value -> the value that will be searched in the table
        return:
            list
    """
    async def get_many(self, key: str, value: any) -> list[Watchable]:
        result = await self._entity.filter(**{key:value})
        return result

    """
        Delete one watchable in the table accordingly to the id provided.

        params:
            id -> the id of the watchable to be deleted
        return
            True -> if success
            False -> if failure
    """
    async def delete(self, watchable: Watchable) -> bool:
        await watchable.delete()
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