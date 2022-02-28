import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.city import UpdateCity

from ..models.user import FullUser, UpdateUser, ViewUser


async def get_user_by_username(
    collection: AsyncIOMotorCollection,
    username: str,
) -> dict | None:
    return await collection.find_one({"username": username})


async def create_user(
    collection: AsyncIOMotorCollection, user: FullUser
) -> dict | None:
    return await collection.insert_one(user.dict())


async def update_user_and_return(
    collection: AsyncIOMotorCollection, user: dict, document: UpdateUser
) -> dict:
    username = user["username"]
    update_user = document.dict()
    update_email = update_user.get("email", user["email"])
    visited_list = update_user["visited_cities"]
    like_to_visit_list = update_user["like_to_visit"]
    print(visited_list, like_to_visit_list, update_email, username)
    return await collection.find_one_and_update(
        {"username": username},
        {
            "$push": {
                "visited_cities": {"$each": visited_list},
                "like_to_visit": {"$each": like_to_visit_list},
            },
        },
        {"$set": {"email": update_email}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
