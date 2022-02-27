from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..core.config import (
    DATABASE_URL,
    DATABASE_NAME,
    CITY_COLLECTION,
    CITY_TEST_COLLECTION,
    USER_COLLECTION,
    USER_TEST_COLLECTION,
)


city_collections = [CITY_COLLECTION, CITY_TEST_COLLECTION]
user_collections = [USER_COLLECTION, USER_TEST_COLLECTION]
unique_indexes = {
    "slug": city_collections,
    "username": user_collections,
}


async def create_indexes(connection: AsyncIOMotorDatabase):
    for field, collections in unique_indexes.items():
        for collection_name in collections:
            collection = connection[collection_name]
            if f"{field}_1" not in await collection.index_information():
                await collection.create_index(field, unique=True)


async def create_connection() -> list[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(DATABASE_URL)
    conn = client[DATABASE_NAME]
    await create_indexes(conn)
    return client, conn
