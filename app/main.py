from fastapi import Body, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware

from .db.schemas import ViewCity, FullCity, InputSight, FullSight, UpdateCity
from .db.crud import (
    get_all_cities,
    get_city_by_slug,
    get_cities_by_rating,
    insert_city_and_return,
    update_city_and_return,
    delete_city_and_return,
)
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
    tags=["city"],
)
async def list_all_cities(limit: int = Query(20, gt=0), skip: int = Query(0, ge=0)):
    return await get_all_cities(conn=app.mongodb, limit=limit, skip=skip)


@app.post(
    "/api/cities",
    response_model=FullCity,
    response_description="Add new city",
    tags=["city"],
)
async def add_city(document: ViewCity = Body(...)):
    return await insert_city_and_return(conn=app.mongodb, document=document)


@app.get(
    "/api/city/{slug}/",
    response_model=ViewCity,
    response_description="Get city",
    tags=["city"],
)
async def get_city(slug: str = Path(..., min_length=1)):
    city = await get_city_by_slug(conn=app.mongodb, slug=slug)
    if city is not None:
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} not found"
    )


@app.put(
    "/api/city/{slug}/",
    response_model=ViewCity,
    response_description="Update city",
    tags=["city"],
)
async def update_city(
    slug: str = Path(..., min_length=1), document: UpdateCity = Body(...)
):
    city = await update_city_and_return(conn=app.mongodb, slug=slug, document=document)
    if city is not None:
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} not found"
    )


@app.delete(
    "/api/city/{slug}/",
    response_description="Delete city",
    tags=["city"],
)
async def delete_city(slug: str = Path(..., min_length=1)):
    await delete_city_and_return(conn=app.mongodb, slug=slug)


@app.get(
    "/api/cities/top/",
    response_model=list[ViewCity],
    response_description="Get the most rated cities",
    tags=["city"],
)
async def get_city_rating(limit: int = Query(20, gt=0), skip: int = Query(0, ge=0)):
    return await get_cities_by_rating(conn=app.mongodb, limit=limit, skip=skip)


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
