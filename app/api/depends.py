"""
Dependencies
"""

from typing import AsyncGenerator

from fastapi import BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine
from app.services import Services


async def get_services(request: Request = None) -> AsyncGenerator[Services, Services]:
    if request:
        yield request.state.services
    else:
        background = BackgroundTasks()
        async with AsyncSession(bind=engine, expire_on_commit=False) as session:
            yield Services(session, background)
            await background()
