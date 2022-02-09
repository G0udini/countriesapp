from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
    Body,
    HTTPException,
    Request,
    status,
)
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from ....core.config import CITY_COLLECTION
from ....crud.city import (
    get_all_cities,
    insert_city_and_return,
    get_city_by_slug,
    update_city_and_return,
    delete_city_and_return,
    get_cities_by_rating,
)
from ....models.city import ViewCity, UpdateCity
from ...shortcuts import ADDITIONAL_CONFLICT_SCHEMA, ADDITIONAL_NOT_FOUND_SCHEMA

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


async def get_mongodb_conn_for_city(request: Request) -> AsyncIOMotorCollection:
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    if not hasattr(request.app.state.mongodb, CITY_COLLECTION):
        raise AttributeError("mongodb client not set on app state")
    return request.app.state.mongodb[CITY_COLLECTION]


@router.get(
    "/",
    response_model=list[ViewCity],
    response_description="List all cities",
)
async def list_all_cities(
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    search: str = Query(None),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await get_all_cities(client=client, limit=limit, skip=skip, search=search)


@router.post(
    "/",
    response_model=ViewCity,
    status_code=status.HTTP_201_CREATED,
    response_description="Add new city",
    responses=ADDITIONAL_CONFLICT_SCHEMA,
)
async def add_city(
    document: ViewCity = Body(...),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    try:
        res = await insert_city_and_return(client=client, document=document)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City '{document.name}' already exists",
        )
    return res


@router.get(
    "/{slug}",
    response_model=ViewCity,
    response_description="Get city",
    responses=ADDITIONAL_NOT_FOUND_SCHEMA,
)
async def get_city(
    slug: str = Path(..., min_length=1),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    city = await get_city_by_slug(client=client, slug=slug)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} was not found"
        )
    return city


@router.put(
    "/{slug}",
    response_model=ViewCity,
    response_description="Update city",
    responses=ADDITIONAL_NOT_FOUND_SCHEMA,
)
async def update_city(
    slug: str = Path(..., min_length=1),
    document: UpdateCity = Body(...),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    city = await update_city_and_return(client=client, slug=slug, document=document)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} was not found"
        )
    return city


@router.delete(
    "/{slug}",
    response_model=ViewCity,
    response_description="Delete city",
    responses=ADDITIONAL_NOT_FOUND_SCHEMA,
)
async def delete_city(
    slug: str = Path(..., min_length=1),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    city = await delete_city_and_return(client=client, slug=slug)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} was not found"
        )
    return city


@router.get(
    "/top/",
    response_model=list[ViewCity],
    response_description="Get the most rated cities",
)
async def get_city_rating(
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    client: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await get_cities_by_rating(client=client, limit=limit, skip=skip)
