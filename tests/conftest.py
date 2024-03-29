import asyncio
from typing import Any, AsyncGenerator, Callable, Generator

import pytest
from httpx import AsyncClient
from redis.client import Redis
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from app import app
from app.core.config import settings
from app.database import Base

engine_test = create_async_engine(settings.pg_dns, poolclass=NullPool)
Base.metadata.bind = engine_test


@pytest.fixture(scope='session', autouse=True)
async def prepare_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session', autouse=True)
def prepare_redis() -> Generator[Redis, Redis, None]:
    redis: Redis = settings.redis
    redis.flushdb()
    yield redis
    redis.flushdb()


@pytest.fixture(scope='session')
def store() -> dict[str, Any]:
    return {}


@pytest.fixture(scope='session')
def cascades() -> dict[int, dict[int, list]]:
    return {}


def reverse(view: Callable, **params) -> str:
    for route in app.routes:
        if route.name == view.__name__:
            return route.path.format(**params)
    raise Exception


@pytest.fixture(scope='session')
async def test_client() -> AsyncGenerator[AsyncClient, AsyncClient]:
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000') as client:
        yield client


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
