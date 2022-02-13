from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.base import create_connection
from .api.api_v1.api import router

app = FastAPI()
app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    state = app.state
    state.mongodb_client, state.mongodb = await create_connection()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.mongodb_client.close()
