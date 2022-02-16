import pymongo
from slugify import slugify

from motor.motor_asyncio import AsyncIOMotorCollection
from ..models.city import ViewCity, UpdateCity


async def get_all_cities(
    collection: AsyncIOMotorCollection,
    limit: int,
    skip: int,
    search: str | None,
) -> list:
    if search:
        return await collection.find(
            {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                ]
            },
            skip=skip,
        ).to_list(length=limit)
    return await collection.find(skip=skip).to_list(length=limit)


async def get_city_by_slug(
    collection: AsyncIOMotorCollection, slug: str
) -> dict | None:
    return await collection.find_one({"slug": slug})


async def insert_city_and_return(
    collection: AsyncIOMotorCollection, document: ViewCity
) -> dict:
    city_doc = document.dict()
    city_doc["slug"] = slugify(city_doc["name"])
    result = await collection.insert_one(city_doc)
    city_doc.update({"_id": result.inserted_id})
    return city_doc


async def update_city_and_return(
    collection: AsyncIOMotorCollection,
    slug: str,
    document: UpdateCity,
) -> dict | None:
    city_doc = document.dict(exclude_unset=True)
    if "name" in city_doc:
        city_doc["slug"] = slugify(city_doc["name"])
    return await collection.find_one_and_update(
        {"slug": slug}, {"$set": city_doc}, return_document=pymongo.ReturnDocument.AFTER
    )


async def delete_city_and_return(
    collection: AsyncIOMotorCollection, slug: str
) -> dict | None:
    return await collection.find_one_and_delete({"slug": slug})


async def get_cities_by_rating(
    collection: AsyncIOMotorCollection, limit: int, skip: int
) -> list[dict]:
    return (
        await collection.find()
        .sort("rating", pymongo.DESCENDING)
        .skip(skip)
        .to_list(length=limit)
    )
