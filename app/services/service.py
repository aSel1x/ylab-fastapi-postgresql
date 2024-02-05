from sqlalchemy.ext.asyncio import AsyncSession

from .services import *


class Services:

    session: AsyncSession

    menu: MenuService
    submenu: SubmenuService
    dish: DishService

    def __init__(
            self,
            session: AsyncSession,
            menu: MenuService = None,
            submenu: SubmenuService = None,
            dish: DishService = None,
    ):
        self.menu = menu or MenuService(session)
        self.submenu = submenu or SubmenuService(session)
        self.dish = dish or DishService(session)
