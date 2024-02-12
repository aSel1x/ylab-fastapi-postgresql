import abc
from typing import Generic, TypeVar

from fastapi import BackgroundTasks
from pydantic import BaseModel

from app.core.redis.repositories import RedisRepository
from app.database import Base
from app.database.repositories import Repository

AbstractModel = TypeVar('AbstractModel', bound=Base)
AbstractScheme = TypeVar('AbstractScheme', bound=BaseModel)


class BaseService(Generic[AbstractModel]):
    type_model: type[Base]
    redis_repository: RedisRepository[AbstractModel]
    db_repository: Repository[AbstractModel]
    background: BackgroundTasks

    def __init__(
            self,
            type_model: type[Base],
            redis_repository: RedisRepository[AbstractModel],
            db_repository: Repository[AbstractModel],
            background: BackgroundTasks,
    ):
        self.type_model = type_model
        self.redis_repository = redis_repository
        self.db_repository = db_repository
        self.background = background

    async def get_id(self, ident: int | str) -> AbstractModel | AbstractScheme | None:
        from_redis: AbstractScheme | None = await self.redis_repository.get(ident)
        if from_redis:
            return from_redis
        if from_db := await self.db_repository.get(ident):
            self.background.add_task(self.redis_repository.save, model=from_db)
            return from_db
        else:
            return None

    async def delete(self, ident: int | str) -> None:
        self.background.add_task(self.redis_repository.delete, ident=ident)
        await self.db_repository.delete(ident)

    async def update(self, ident: int | str, scheme: AbstractScheme) -> AbstractModel | None:
        await self.db_repository.update(ident, **scheme.__dict__)
        if not (new_model := await self.db_repository.get(ident)):
            return None
        self.background.add_task(self.redis_repository.update, model=new_model)
        return new_model

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> AbstractModel:
        ...
