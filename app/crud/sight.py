import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection
from slugify import slugify
from pymongo.errors import DuplicateKeyError

from ..models.sight import ViewSight, UpdateSight
from .city import get_city_by_slug


async def get_sights_by_city_slug(
    collection: AsyncIOMotorCollection, slug: str, limit: int, skip: int
) -> list[dict] | None:
    city = await get_city_by_slug(collection, slug)
    return city["sights"][skip : skip + limit]


async def insert_sight_and_return(
    collection: AsyncIOMotorCollection, slug: str, document: ViewSight
) -> dict:
    sight = document.dict()
    sight_slug = slugify(sight["name"])
    sight["slug"] = sight_slug
    result = await collection.update_one(
        {"slug": slug, "sights.slug": {"$ne": sight_slug}},
        {
            "$push": {
                "sights": {
                    "$each": [sight],
                    "$sort": {"rating": -1, "number_of_scores": -1},
                }
            }
        },
    )
    if result.matched_count:
        return sight
    raise DuplicateKeyError("Match with existed slug field")


async def get_sight_and_return(
    collection: AsyncIOMotorCollection, city_slug: str, sight_slug: str
) -> dict | None:
    if sight_doc := await collection.find_one(
        {"slug": city_slug, "sights.slug": sight_slug}, {"_id": 0, "sights.$": 1}
    ):
        return sight_doc["sights"][0]


async def update_sight_and_return(
    collection: AsyncIOMotorCollection,
    city_slug: str,
    sight_slug: str,
    document: UpdateSight,
) -> dict | None:
    sight_doc = document.dict(exclude_unset=True)
    if "name" in sight_doc:
        sight_doc["slug"] = slugify(sight_doc["name"])
        if await get_sight_and_return(collection, city_slug, sight_slug):
            raise DuplicateKeyError("Match with existed slug field")

    sight = await collection.find_one_and_update(
        {"slug": city_slug, "sights.slug": sight_slug},
        {"$set": {f"sights.$.{key}": val for key, val in sight_doc.items()}},
        projection={"_id": 0, "sights.$": 1},
    )
    if sight:
        sight = sight["sights"][0]
        sight.update(**sight_doc)
        return sight


async def delete_sight_and_return(
    collection: AsyncIOMotorCollection, city_slug: str, sight_slug: str
) -> dict | None:

    if result := await collection.find_one_and_update(
        {"slug": city_slug},
        {"$pull": {"sights": {"slug": sight_slug}}},
        return_document=pymongo.ReturnDocument.BEFORE,
    ):
        for sight in result["sights"]:
            print(sight["slug"], sight)
            if sight["slug"] == sight_slug:
                return sight
