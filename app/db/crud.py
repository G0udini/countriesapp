from .base import AsyncIOMotorClient
from ..core.config import CITY_COLLECTION

from slugify import slugify
from bson import ObjectId


async def get_all_cities(conn: AsyncIOMotorClient) -> list:
    return await conn[CITY_COLLECTION].find().to_list(length=100)
