import pytest

from typing import AsyncGenerator, Dict, Any
from httpx import AsyncClient

from app.__main__ import app
from app.db.database import DataBase

db = DataBase()


@pytest.fixture(scope="session")
async def server():
    await db.connection.setup()
    yield
    await db.connection.drop()


@pytest.fixture(scope="session")
def store() -> Dict[str, Any]:
    return {}


@pytest.fixture(scope="session")
def cascades() -> Dict[int, Dict[int, list]]:
    return {}


@pytest.fixture(scope="function")
async def test_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/test-api/v1') as client:
        yield client
