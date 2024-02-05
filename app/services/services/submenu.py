"""
Submenu service.
"""
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis.repositories import SubmenuRedisRepository
from app.database.models import Submenu
from app.database.repositories import SubmenuRepository
from app.schemas import SubmenuScheme

from .base import BaseService


class SubmenuService(BaseService[Submenu]):

    redis_repository: SubmenuRedisRepository
    db_repository: SubmenuRepository

    def __init__(self, session: AsyncSession):
        super().__init__(
            type_model=Submenu,
            redis_repository=SubmenuRedisRepository(),
            db_repository=SubmenuRepository(session)
        )

    async def new(
            self,
            title: str,
            description: str,
            menu_id: int,
    ) -> Submenu:
        new_submenu = await self.db_repository.new(
            title=title,
            description=description,
            menu_id=menu_id,
        )
        await self.redis_repository.save(new_submenu)
        return new_submenu

    async def get_by_menu_id(self, menu_id: int | str) -> Sequence[Submenu] | Sequence[SubmenuScheme]:
        cache = await self.redis_repository.get_by_menu_id(menu_id)
        if cache is not None:
            return cache
        return await self.db_repository.get_by_menu_id(menu_id)
