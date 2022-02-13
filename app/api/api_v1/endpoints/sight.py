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

from ....crud.sight import get_sights_by_city_slug, insert_sight_and_return
from ....db.dependencies import get_mongodb_conn_for_city
from ....models.sight import ViewSight
from ....models.shortcuts import ADDITIONAL_CONFLICT_SIGHT_SCHEMA


router = APIRouter(
    prefix="/cities",
    tags=["sights"],
)


@router.get(
    "/{city}/sight/",
    response_model=list[ViewSight],
    response_description="List all corresponding sights",
)
async def list_sights(
    city: str = Path(..., min_length=1),
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await get_sights_by_city_slug(
        collection=collection, slug=city, limit=limit, skip=skip
    )


@router.post(
    "/{city}/sight/",
    response_model=ViewSight,
    status_code=status.HTTP_201_CREATED,
    response_description="Add sight to city",
    responses=ADDITIONAL_CONFLICT_SIGHT_SCHEMA,
)
async def post_sight(
    city: str = Path(..., min_length=1),
    document: ViewSight = Body(...),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    try:
        res = await insert_sight_and_return(
            collection=collection, slug=city, document=document
        )
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sight '{document.name}' already exists",
        ) from e
    return res


@router.get(
    "/{city}/sight/{sight}",
    response_model=ViewSight,
    response_description="Get sight",
    # responses=ADDITIONAL_CONFLICT_CITY_SCHEMA,
)
async def get_sight(
    slug: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return {"hello here"}


@router.put("/{city}/sight/{sight}")
async def update_sight(
    slug: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return {"hello here"}


@router.delete("/{city}/sight/{sight}")
async def delete_sight(
    slug: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return {"hello here"}
