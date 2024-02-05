"""
Dependencies
"""

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine
from app.services import Services


async def get_services(request: Request = None) -> Services:
    if request:
        return request.state.services
    else:
        async with AsyncSession(bind=engine, expire_on_commit=False) as session:
            return Services(session)
