from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.user import FullUser


async def get_user_by_username(
    collection: AsyncIOMotorCollection,
    username: str,
) -> dict | None:
    return await collection.find_one({"username": username})


async def create_user(
    collection: AsyncIOMotorCollection, user: FullUser
) -> dict | None:
    return await collection.insert_one(user.dict())
