from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.user import RegisterUser


async def get_user_by_username(
    collection: AsyncIOMotorCollection,
    username: str,
) -> dict | None:
    return await collection.find_one({"username": username})


async def create_user(
    collection: AsyncIOMotorCollection, form: RegisterUser
) -> dict | None:
    user = form.dict()
    del user["password2"]
    print(user)
    return await collection.insert_one(user)
