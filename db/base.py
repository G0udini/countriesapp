import os
import motor.motor_asyncio

from ..main import app

DATABASE_URL = os.getenv("DB_URL")

DATABASE_NAME = os.getenv("DB_NAME")


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    app.mongodb = app.mongodb_client[DATABASE_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
