import abc
from typing import Generic, TypeVar

from app.core.redis.repositories import RedisRepository
from app.database import Base
from app.database.repositories import Repository
from app.schemas import BaseScheme

AbstractModel = TypeVar('AbstractModel', bound=Base)
AbstractScheme = TypeVar('AbstractScheme', bound=BaseScheme)


class BaseService(Generic[AbstractModel]):
    type_model: type[Base]
    redis_repository: RedisRepository[AbstractModel]
    db_repository: Repository[AbstractModel]

    def __init__(
            self,
            type_model: type[Base],
            redis_repository: RedisRepository[AbstractModel],
            db_repository: Repository[AbstractModel]
    ):
        self.type_model = type_model
        self.redis_repository = redis_repository
        self.db_repository = db_repository

    async def get_id(self, ident: int | str) -> AbstractModel | AbstractScheme | None:
        from_redis: AbstractScheme | None = await self.redis_repository.get(ident)
        if from_redis is not None:
            return from_redis
        from_db: AbstractModel | None = await self.db_repository.get(ident)
        if from_db is not None:
            await self.redis_repository.save(from_db)
            return from_db
        return None

    async def delete(self, ident: int | str) -> None:
        await self.redis_repository.delete(ident)
        await self.db_repository.delete(ident)

    async def update(self, ident: int | str, scheme: AbstractScheme) -> AbstractModel | None:
        await self.db_repository.update(ident, **scheme.__dict__)
        new_model: AbstractModel | None = await self.db_repository.get(ident)
        if new_model is None:
            return None
        await self.redis_repository.save(new_model)
        return new_model

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> AbstractModel:
        ...
