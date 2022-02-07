import pymongo
from slugify import slugify
from bson import ObjectId

from ..db.base import AsyncIOMotorClient
from ..models.city import ViewCity, UpdateCity


async def get_all_cities(
    client: AsyncIOMotorClient,
    limit: int,
    skip: int,
    search: str | None,
) -> list:
    if search:
        return await client.find(
            {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                ]
            },
            skip=skip,
        ).to_list(length=limit)
    return await client.find(skip=skip).to_list(length=limit)


async def get_city_by_slug(client: AsyncIOMotorClient, slug: str) -> dict | None:
    return await client.find_one({"slug": slug})


async def insert_city_and_return(
    client: AsyncIOMotorClient, document: ViewCity
) -> dict:
    city_doc = document.dict()
    city_doc["slug"] = slugify(city_doc["name"])
    await client.insert_one(city_doc)
    return city_doc


async def update_city_and_return(
    client: AsyncIOMotorClient,
    slug: str,
    document: UpdateCity,
) -> dict | None:
    city_doc = document.dict(exclude_unset=True)
    if "name" in city_doc:
        city_doc["slug"] = slugify(city_doc["name"])
    return await client.find_one_and_update(
        {"slug": slug}, {"$set": city_doc}, return_document=pymongo.ReturnDocument.AFTER
    )


async def delete_city_and_return(client: AsyncIOMotorClient, slug: str) -> dict | None:
    return await client.find_one_and_delete({"slug": slug})


async def get_cities_by_rating(
    client: AsyncIOMotorClient, limit: int, skip: int
) -> list[dict]:
    return (
        await client.find()
        .sort("rating", pymongo.DESCENDING)
        .skip(skip)
        .to_list(length=limit)
    )
