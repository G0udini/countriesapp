from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
    Body,
    HTTPException,
    status,
)
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from ....db.dependencies import get_mongodb_conn_for_city
from ....models.city import ViewCity, UpdateCity
from ....models.shortcuts import (
    ADDITIONAL_CONFLICT_CITY_SCHEMA,
    ADDITIONAL_NOT_FOUND_CITY_SCHEMA,
)
from ....crud.city import (
    get_all_cities,
    insert_city_and_return,
    get_city_by_slug,
    update_city_and_return,
    delete_city_and_return,
    get_cities_by_rating,
)

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


@router.get(
    "/",
    response_model=list[ViewCity],
    response_description="List all cities",
)
async def list_all_cities(
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    search: str = Query(None),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await get_all_cities(
        collection=collection, limit=limit, skip=skip, search=search
    )


@router.post(
    "/",
    response_model=ViewCity,
    status_code=status.HTTP_201_CREATED,
    response_description="Add new city",
    responses=ADDITIONAL_CONFLICT_CITY_SCHEMA,
)
async def add_city(
    document: ViewCity = Body(...),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    try:
        res = await insert_city_and_return(collection=collection, document=document)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City '{document.name}' already exists",
        ) from e
    return res


@router.get(
    "/{slug}",
    response_model=ViewCity,
    response_description="Get city",
    responses=ADDITIONAL_NOT_FOUND_CITY_SCHEMA,
)
async def get_city(
    slug: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    if city := await get_city_by_slug(collection=collection, slug=slug):
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"City '{slug}' was not found"
    )


@router.put(
    "/{slug}",
    response_model=ViewCity,
    response_description="Update city",
    responses=ADDITIONAL_NOT_FOUND_CITY_SCHEMA,
)
async def update_city(
    slug: str = Path(..., min_length=1),
    document: UpdateCity = Body(...),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    if city := await update_city_and_return(
        collection=collection, slug=slug, document=document
    ):
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"City '{slug}' was not found"
    )


@router.delete(
    "/{slug}",
    response_model=ViewCity,
    response_description="Delete city",
    responses=ADDITIONAL_NOT_FOUND_CITY_SCHEMA,
)
async def delete_city(
    slug: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    if city := await delete_city_and_return(collection=collection, slug=slug):
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"City '{slug}' was not found"
    )


@router.get(
    "/top/",
    response_model=list[ViewCity],
    response_description="Get the most rated cities",
)
async def get_city_rating(
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await get_cities_by_rating(collection=collection, limit=limit, skip=skip)
