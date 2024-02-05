"""
Submenu repository.
"""
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Menu, Submenu
from .abstract import Repository


class SubmenuRepository(Repository[Submenu]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Submenu, session=session)

    async def new(
            self,
            title: str,
            description: str,
            menu_id: int,
            dishes: list['Dish'] = []
    ) -> Submenu:
        new_submenu = await self.session.merge(
            Submenu(
                title=title,
                description=description,
                menu_id=menu_id,
                dishes=dishes,
            )
        )
        await self.session.commit()
        return new_submenu

    async def get_by_menu_id(self, menu_id: int | str) -> Sequence[Submenu]:
        submenus = await self.get_many(Submenu.menu_id == menu_id)
        return submenus
