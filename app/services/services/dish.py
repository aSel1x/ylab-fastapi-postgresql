"""
Dish service.
"""
from decimal import Decimal
from typing import Sequence

from app.core.redis.repositories import DishRedisRepository
from app.database.models import Dish
from app.database.repositories import DishRepository
from app.schemas import DishScheme

from .base import BaseService


class DishService(BaseService[Dish]):

    type_model: Dish
    redis_repository: DishRedisRepository
    db_repository: DishRepository

    def __init__(self, session):
        super().__init__(
            type_model=Dish,
            redis_repository=DishRedisRepository(),
            db_repository=DishRepository(session),
        )

    async def new(
            self,
            title: str,
            description: str,
            price: Decimal,
            submenu_id: int
    ) -> Dish:
        new_dish = await self.db_repository.new(
            title=title,
            description=description,
            price=price,
            submenu_id=submenu_id,
        )
        await self.redis_repository.save(new_dish)
        return new_dish

    async def get_by_submenu_id(self, submenu_id: int | str) -> Sequence[Dish] | Sequence[DishScheme]:
        cache = await self.redis_repository.get_by_submenu_id(submenu_id)
        if cache is not None:
            return cache
        return await self.db_repository.get_by_submenu_id(submenu_id)
