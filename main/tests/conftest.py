import asyncio
import pytest

from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main.data_base.MongoAPI import MongoDbApi
from main.routers.routes.notes import router as note_router
from main.utils.config import MONGO_TEST_DB_CONNECTION_PATH


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


app = FastAPI()
app.include_router(note_router)

db = MongoDbApi()
db.connect_to_db(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)

# Save ref to db
app.state.db = db


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client
