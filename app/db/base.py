from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..core.config import DATABASE_URL, DATABASE_NAME


async def create_connection() -> list[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(DATABASE_URL)
    conn = client[DATABASE_NAME]
    return client, conn
