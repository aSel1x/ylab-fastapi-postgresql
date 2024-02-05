"""
Menu service.
"""
from typing import Sequence

from app.core.redis.repositories import MenuRedisRepository
from app.database.models import Menu
from app.database.repositories import MenuRepository
from app.schemas import MenuScheme

from .base import BaseService


class MenuService(BaseService[Menu]):

    type_model: Menu
    redis_repository: MenuRedisRepository
    db_repository: MenuRepository

    def __init__(self, session):
        super().__init__(
            type_model=Menu,
            redis_repository=MenuRedisRepository(),
            db_repository=MenuRepository(session),
        )

    async def new(
            self,
            title: str,
            description: str,
    ) -> Menu:
        new_menu = await self.db_repository.new(
            title=title,
            description=description,
        )
        await self.redis_repository.save(new_menu)
        return new_menu

    async def get_all(self) -> Sequence[Menu] | Sequence[MenuScheme]:
        cache = await self.redis_repository.get_all()
        if cache is not None:
            return cache
        return await self.db_repository.get_many()
