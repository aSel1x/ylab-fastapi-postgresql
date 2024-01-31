from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.data.config import DB_ORM_URL

engine = create_async_engine(DB_ORM_URL)


async def get_async_session():
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close_all()
            await engine.dispose()
