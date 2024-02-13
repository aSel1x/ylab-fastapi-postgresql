"""
Menu service.
"""
from typing import Sequence

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis.repositories import MenuRedisRepository
from app.database.models import Menu
from app.database.repositories import MenuRepository
from app.schemas import MenuScheme
from app.schemas.extra import MenuPlus

from .base import BaseService
from .discount import DiscountService


class MenuService(BaseService[Menu]):

    session: AsyncSession
    background: BackgroundTasks

    redis_repository: MenuRedisRepository
    db_repository: MenuRepository

    def __init__(self, session, background):
        super().__init__(
            type_model=Menu,
            background=background,
            redis_repository=MenuRedisRepository(),
            db_repository=MenuRepository(session),
        )
        self.background = background
        self.discount_service = DiscountService()

    async def new(
            self,
            title: str,
            description: str,
    ) -> Menu:
        new_menu = await self.db_repository.new(
            title=title,
            description=description,
        )
        self.background.add_task(self.redis_repository.save, new_menu)
        return new_menu

    async def get_all(self) -> Sequence[Menu | MenuScheme]:
        if cache := await self.redis_repository.get_all():
            return cache
        return await self.db_repository.get_many()

    async def get_all_extra(self) -> Sequence[Menu | MenuPlus]:
        data: Sequence[MenuPlus | Menu] = (
            await self.redis_repository.get_all_extra() or await self.db_repository.get_many()
        )
        for menu in data:
            for submenu in menu.submenus:
                submenu.dishes = [
                    await self.discount_service.aggregate_prices(dish=dish) for dish in submenu.dishes
                ]

        return data
