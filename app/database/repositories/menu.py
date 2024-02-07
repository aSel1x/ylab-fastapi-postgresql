"""
Menu repository.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Menu, Submenu
from .abstract import Repository


class MenuRepository(Repository[Menu]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Menu, session=session)

    async def new(
            self,
            title: str,
            description: str,
            submenus: list['Submenu'] = [],
    ) -> Menu:
        new_menu = await self.session.merge(
            Menu(
                title=title,
                description=description,
                submenus=submenus,
            )
        )
        await self.session.commit()
        return new_menu
