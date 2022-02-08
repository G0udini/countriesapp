from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..core.config import (
    DATABASE_URL,
    DATABASE_NAME,
    CITY_COLLECTION,
    CITY_TEST_COLLECTION,
)

collections = [CITY_COLLECTION, CITY_TEST_COLLECTION]


async def create_connection() -> list[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(DATABASE_URL)
    conn = client[DATABASE_NAME]
    for collection in collections:
        col_tmp = conn[collection]
        if "slug_1" not in await col_tmp.index_information():
            await col_tmp.create_index("slug", unique=True)
    return client, conn
