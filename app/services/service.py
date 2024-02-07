from sqlalchemy.ext.asyncio import AsyncSession

from .services import DishService, MenuService, SubmenuService


class Services:

    session: AsyncSession

    menu: MenuService
    submenu: SubmenuService
    dish: DishService

    def __init__(
            self,
            session: AsyncSession,
            menu: MenuService | None = None,
            submenu: SubmenuService | None = None,
            dish: DishService | None = None,
    ):
        self.menu = menu or MenuService(session)
        self.submenu = submenu or SubmenuService(session)
        self.dish = dish or DishService(session)
