from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends, HTTPException, Request

from ..core.security import get_current_user, oauth2_scheme
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


async def get_current_active_user(
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_user),
    token: str = Depends(oauth2_scheme),
):
    current_user = await get_current_user(collection=collection, token=token)
    if current_user["active"]:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")
