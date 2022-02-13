from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Request

from ..core.config import CITY_COLLECTION


async def get_mongodb_conn_for_city(request: Request) -> AsyncIOMotorCollection:
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    if not hasattr(request.app.state.mongodb, CITY_COLLECTION):
        raise AttributeError("mongodb client not set on app state")
    return request.app.state.mongodb[CITY_COLLECTION]
