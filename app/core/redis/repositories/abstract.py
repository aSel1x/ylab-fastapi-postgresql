import abc
import pickle
from typing import Generic, Sequence, TypeVar

from redis import asyncio as aioredis

from app.core.config import settings
from app.database import Base
from app.schemas import BaseScheme

AbstractModel = TypeVar('AbstractModel', bound=Base)
AbstractScheme = TypeVar('AbstractScheme', bound=BaseScheme)


class RedisRepository(Generic[AbstractModel]):
    type_model: type[Base]
    redis = aioredis.from_url(settings.redis_dns)

    def __init__(
            self,
            type_model: type[Base],
            redis: aioredis.Redis = redis
    ):
        self.type_model = type_model
        self.redis = redis

    async def get(self, ident: int | str) -> AbstractScheme | None:
        key = f'{self.type_model.__name__}:{ident}'
        encoded_data = await self.redis.get(key)
        if encoded_data is None:
            return
        return pickle.loads(encoded_data)

    async def _delete(self, ident: int | str) -> AbstractScheme | None:
        key = f'{self.type_model.__name__}:{ident}'
        encoded_data = await self.redis.get(key)
        await self.redis.delete(key)
        if encoded_data is None:
            return
        return pickle.loads(encoded_data)

    async def get_all(self) -> Sequence[AbstractScheme] | None:
        # AnyModel:*
        any_list = []
        keys = await self.redis.keys(f'{self.type_model.__name__}:*')
        for key in keys:
            encoded_data = await self.redis.get(key)
            any_list.append(pickle.loads(encoded_data))
        return any_list if any_list != [] else None

    @abc.abstractmethod
    async def delete(self, ident: int | str) -> None:
        ...

    @abc.abstractmethod
    async def save(self, model: AbstractModel) -> None:
        ...
