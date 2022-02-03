from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .db.schemas import ViewCity, FullCity, InputSight, FullSight
from .db.crud import get_all_cities
from .db.base import create_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client, app.mongodb = await create_connection()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get(
    "/api/cities/",
    response_model=list[ViewCity],
    response_description="List all cities",
)
async def list_all_cities(request: Request):
    return await get_all_cities(conn=app.mongodb)


# @app.get("/api/todo/{id}", response_model=ResponseTodo)
# async def get_todo_by_id(id: int):
#     pass


# @app.post("/api/todo/", response_model=ResponseTodo)
# async def post_todo():
#     pass


# @app.put("/api/todo/{id}", response_model=ResponseTodo)
# async def update_todo(id: int, data: dict):
#     pass


# @app.delete("/api/todo/{id}", response_model=ResponseTodo)
# async def delete_todo(id: int):
#     pass