from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from app.core.config import settings
from app.database.repositories import DishRepository, MenuRepository, SubmenuRepository


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=False, pool_pre_ping=True)


engine = create_async_engine(settings.pg_dns)


class Database:
    session: AsyncSession

    menu: MenuRepository
    submenu: SubmenuRepository
    dish: DishRepository

    def __init__(
            self,
            session: AsyncSession,
            menu: MenuRepository = None,
            submenu: SubmenuRepository = None,
            dish: DishRepository = None,
    ):
        self.session = session
        self.menu = menu or MenuRepository(session=session)
        self.submenu = submenu or SubmenuRepository(session=session)
        self.dish = dish or DishRepository(session=session)
