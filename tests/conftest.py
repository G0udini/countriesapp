import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorCollection

from app.main import app
from app.core.config import CITY_TEST_COLLECTION
from app.api.api_v1.endpoints.city import get_mongodb_conn_for_city


async def get_test_mongodb_conn_for_city(request: Request) -> AsyncIOMotorCollection:
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    if not hasattr(request.app.state.mongodb, CITY_TEST_COLLECTION):
        raise AttributeError("mongodb client not set on app state")
    return request.app.state.mongodb[CITY_TEST_COLLECTION]


app.dependency_overrides[get_mongodb_conn_for_city] = get_test_mongodb_conn_for_city


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
