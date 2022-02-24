from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Request

from ..core.config import CITY_COLLECTION, USER_COLLECTION


async def check_attributes(request: Request, attr: str):
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    if not hasattr(request.app.state.mongodb, attr):
        raise AttributeError("mongodb client not set on app state")


async def get_mongodb_conn_for_city(request: Request) -> AsyncIOMotorCollection:
    await check_attributes(request, CITY_COLLECTION)
    return request.app.state.mongodb[CITY_COLLECTION]


async def get_mongodb_conn_for_user(request: Request) -> AsyncIOMotorCollection:
    await check_attributes(request, USER_COLLECTION)
    return request.app.state.mongodb[USER_COLLECTION]
