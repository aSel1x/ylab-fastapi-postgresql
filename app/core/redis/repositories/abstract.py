import abc
import pickle
from typing import Generic, TypeVar

from pydantic import BaseModel
from redis import asyncio as aioredis

from app.core.config import settings
from app.database import Base
from app.schemas import BaseScheme

AbstractModel = TypeVar('AbstractModel', bound=Base)
AbstractScheme = TypeVar('AbstractScheme', bound=BaseModel)


class RedisRepository(Generic[AbstractModel]):
    type_model: type[Base]
    type_scheme: type[BaseScheme]
    redis = aioredis.from_url(settings.redis_dns)

    def __init__(
            self,
            type_model: type[Base],
            type_scheme: type[BaseScheme],
            redis: aioredis.Redis = redis
    ):
        self.type_model = type_model
        self.type_scheme = type_scheme
        self.redis = redis

    async def get(self, ident: int | str) -> AbstractScheme | None:
        key = f'{self.type_model.__name__}:{ident}'
        encoded_data = await self.redis.get(key)
        if isinstance(encoded_data, bytes):
            decoded_data: AbstractScheme = pickle.loads(encoded_data)
            return decoded_data
        return None

    async def pre_delete(self, ident: int | str) -> AbstractScheme | None:
        key = f'{self.type_model.__name__}:{ident}'
        encoded_data = await self.redis.get(key)
        if isinstance(encoded_data, bytes):
            decoded_data: AbstractScheme = pickle.loads(encoded_data)
            await self.redis.delete(key)
            return decoded_data
        return None

    async def update(self, model: AbstractModel) -> None:
        await self.redis.set(
            name=f'{self.type_model.__name__}:{model.id}',
            value=pickle.dumps(self.type_scheme(**model.to_dict()))
        )

    @abc.abstractmethod
    async def delete(self, ident: int | str) -> None:
        ...

    @abc.abstractmethod
    async def save(self, model: AbstractModel) -> None:
        ...
