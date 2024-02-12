"""
Dish service.
"""
from decimal import Decimal
from typing import Sequence

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis.repositories import DishRedisRepository
from app.database.models import Dish
from app.database.repositories import DishRepository
from app.schemas import DishScheme

from .base import BaseService
from .discount import DiscountService


class DishService(BaseService[Dish]):

    session: AsyncSession
    background: BackgroundTasks

    redis_repository: DishRedisRepository
    db_repository: DishRepository

    discount_service: DiscountService

    def __init__(self, session, background):
        super().__init__(
            type_model=Dish,
            redis_repository=DishRedisRepository(),
            db_repository=DishRepository(session),
            background=background,
        )
        self.discount_service = DiscountService()

    async def new(
            self,
            title: str,
            description: str,
            price: Decimal | str,
            submenu_id: int
    ) -> Dish:
        new_dish = await self.db_repository.new(
            title=title,
            description=description,
            price=price,
            submenu_id=submenu_id,
        )
        self.background.add_task(self.redis_repository.save, new_dish)
        return new_dish

    async def get_id(self, ident: int | str) -> Dish | DishScheme | None:
        from_redis: DishScheme | None = await self.redis_repository.get(ident)
        if from_redis:
            return await self.discount_service.aggregate_prices(from_redis)
        elif from_db := await self.db_repository.get(ident):
            self.background.add_task(self.redis_repository.save, model=from_db)
            return await self.discount_service.aggregate_prices(from_db)
        else:
            return None

    async def get_by_submenu_id(self, submenu_id: int | str) -> Sequence[Dish] | Sequence[DishScheme]:
        if cache := await self.redis_repository.get_by_submenu_id(submenu_id):
            return [await self.discount_service.aggregate_prices(dish) for dish in cache]
        return [await self.discount_service.aggregate_prices(dish) for dish
                in await self.db_repository.get_by_submenu_id(submenu_id)]
