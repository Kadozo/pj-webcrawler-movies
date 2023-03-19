from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.genre.model import Genre

class GenreRepository:
    def __init__(self):
        self._entity = Genre
        self._model_creator = pydantic_model_creator(Genre)

    """
        Transform a genre object in a dictionary

        params:
            genre -> the genre object
        return:
            dictionary with the attributes of the genre object passed
    """
    async def to_dict(self, genre: Genre) -> dict:
        result = await self._model_creator.from_tortoise_orm(genre)
        return result.dict()

    """
        Create a new Genre

        params:
            genre dict with the type and value of the genre
        return:
            Object Genre -> if success
            None -> if failure
    """
    async def create(self, genre: dict) -> Genre:
        return await self._entity.create(**genre)
    

    """
        Update a Genre

        params:
            genre -> the genre to update
            data -> a dictionary with the new data to update
        return:
            O genre atualizado
        raises:
            ConfigurationError -> Configuration error
            ValueError -> When a passed parameter is not type compatible.
    """
    async def update(self, genre: Genre, data: dict) -> Genre:
        result = await genre.update_from_dict(data)
        return result

    """
        Get one genre where it has the same id as given.

        params:
            id of the genre wanted
        return:
            Object Genre found or None if not found
    """
    async def get_one(self, id: int) -> Genre:
        result = await self._entity.get_or_none(id=id)
        return result
    
    """
        Get all genres in the table

        return:
            list
    """
    async def get_all(self) -> list[Genre]:
        result = await self._entity.all()
        return result
    
    """
        Get one or more genre in the table accordingly to key and value provided.

        params:
            key -> the key that will be searched in the table
            value -> the value that will be searched in the table
        return:
            list
    """
    async def get_many(self, key: str, value: any) -> list[Genre]:
        result = await self._entity.filter(**{key:value})
        return result

    """
        Delete one genre in the table accordingly to the id provided.

        params:
            id -> the id of the genre to be deleted
        return
            True -> if success
            False -> if failure
    """
    async def delete(self, genre: Genre) -> bool:
        await genre.delete()
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