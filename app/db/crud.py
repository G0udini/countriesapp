from .base import AsyncIOMotorClient
from ..core.config import CITY_COLLECTION
from .schemas import FullCity, ViewCity, UpdateCity

import pymongo
from slugify import slugify
from bson import ObjectId


async def get_all_cities(
    conn: AsyncIOMotorClient, limit: int, skip: int
) -> list[ViewCity]:
    return await conn[CITY_COLLECTION].find(skip=skip).to_list(length=limit)


async def get_city_by_slug(conn: AsyncIOMotorClient, slug: str) -> ViewCity:
    return await conn[CITY_COLLECTION].find_one({"slug": slug})


async def get_cities_by_rating(
    conn: AsyncIOMotorClient, limit: int, skip: int
) -> list[ViewCity]:
    return (
        await conn[CITY_COLLECTION]
        .find()
        .sort("rating", pymongo.DESCENDING)
        .skip(skip)
        .to_list(length=limit)
    )


async def insert_city_and_return(conn: AsyncIOMotorClient, document: ViewCity):
    city_doc = document.dict()
    city_doc["slug"] = slugify(city_doc["name"])
    await conn[CITY_COLLECTION].insert_one(city_doc)
    return city_doc


async def update_city_and_return(
    conn: AsyncIOMotorClient, slug: str, document: UpdateCity
):
    city_doc = document.dict(exclude_unset=True)
    if "name" in city_doc:
        city_doc["slug"] = slugify(city_doc["name"])
    return await conn[CITY_COLLECTION].find_one_and_update(
        {"slug": slug}, {"$set": city_doc}, return_document=pymongo.ReturnDocument.AFTER
    )


async def delete_city_and_return(conn: AsyncIOMotorClient, slug: str):
    await conn[CITY_COLLECTION].delete_one({"slug": slug})
