from .base import AsyncIOMotorClient
from ..core.config import CITY_COLLECTION
from .schemas import ViewCity, UpdateCity

import pymongo
from slugify import slugify
from bson import ObjectId


async def get_all_cities(
    conn: AsyncIOMotorClient, limit: int, skip: int, search: str | None
) -> list:
    if search:
        return (
            await conn[CITY_COLLECTION]
            .find(
                {
                    "$or": [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"description": {"$regex": search, "$options": "i"}},
                    ]
                },
                skip=skip,
            )
            .to_list(length=limit)
        )
    return await conn[CITY_COLLECTION].find(skip=skip).to_list(length=limit)


async def get_city_by_slug(conn: AsyncIOMotorClient, slug: str) -> dict | None:
    return await conn[CITY_COLLECTION].find_one({"slug": slug})


async def insert_city_and_return(conn: AsyncIOMotorClient, document: ViewCity) -> dict:
    city_doc = document.dict()
    city_doc["slug"] = slugify(city_doc["name"])
    await conn[CITY_COLLECTION].insert_one(city_doc)
    return city_doc


async def update_city_and_return(
    conn: AsyncIOMotorClient, slug: str, document: UpdateCity
) -> dict | None:
    city_doc = document.dict(exclude_unset=True)
    if "name" in city_doc:
        city_doc["slug"] = slugify(city_doc["name"])
    return await conn[CITY_COLLECTION].find_one_and_update(
        {"slug": slug}, {"$set": city_doc}, return_document=pymongo.ReturnDocument.AFTER
    )


async def delete_city_and_return(conn: AsyncIOMotorClient, slug: str) -> dict | None:
    return await conn[CITY_COLLECTION].find_one_and_delete({"slug": slug})


async def get_cities_by_rating(
    conn: AsyncIOMotorClient, limit: int, skip: int
) -> list[dict]:
    return (
        await conn[CITY_COLLECTION]
        .find()
        .sort("rating", pymongo.DESCENDING)
        .skip(skip)
        .to_list(length=limit)
    )
