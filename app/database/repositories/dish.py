"""
Dish repository.
"""
from decimal import Decimal
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Dish
from .abstract import Repository


class DishRepository(Repository[Dish]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Dish, session=session)

    async def new(
        self,
        title: str,
        description: str,
        price: Decimal | str,
        submenu_id: int
    ) -> Dish:
        new_dish = await self.session.merge(
            Dish(
                title=title,
                description=description,
                price=price,
                submenu_id=submenu_id,
            )
        )
        await self.session.commit()
        return new_dish

    async def get_by_submenu_id(self, submenu_id: int | str) -> Sequence[Dish]:
        submenus = await self.get_many(Dish.submenu_id == submenu_id)
        return submenus
