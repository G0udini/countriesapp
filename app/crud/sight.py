from motor.motor_asyncio import AsyncIOMotorCollection
from slugify import slugify
from pymongo.errors import DuplicateKeyError

from ..models.sight import ViewSight
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


# db.coll.update(
#     {_id: id, 'profile_set.name': {$ne: 'nick'}},
#     {$push: {profile_set: {'name': 'nick', 'options': 2}}})
