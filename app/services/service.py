from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from .services import DishService, MenuService, SubmenuService


class Services:

    session: AsyncSession
    background: BackgroundTasks

    menu: MenuService
    submenu: SubmenuService
    dish: DishService

    def __init__(
            self,
            session: AsyncSession,
            background: BackgroundTasks,
            menu: MenuService | None = None,
            submenu: SubmenuService | None = None,
            dish: DishService | None = None,
    ):
        self.menu = menu or MenuService(session, background)
        self.submenu = submenu or SubmenuService(session, background)
        self.dish = dish or DishService(session, background)
