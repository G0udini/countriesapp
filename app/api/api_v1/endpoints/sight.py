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
from ....models.sight import ViewSight, UpdateSight
from ....models.shortcuts import (
    ADDITIONAL_CONFLICT_SIGHT_SCHEMA,
    ADDITIONAL_NOT_FOUND_SIGHT_SCHEMA,
)
from ....crud.sight import (
    get_sights_by_city_slug,
    insert_sight_and_return,
    get_sight_and_return,
    update_sight_and_return,
)


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
    responses=ADDITIONAL_NOT_FOUND_SIGHT_SCHEMA,
)
async def get_sight(
    city: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    if returned_sight := await get_sight_and_return(
        collection=collection, slug=city, sight=sight
    ):
        return returned_sight
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sight '{sight}' was not found",
    )


@router.put("/{city}/sight/{sight}")
async def update_sight(
    city: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    document: UpdateSight = Body(...),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return await update_sight_and_return(
        collection=collection, slug=city, sight=sight, document=document
    )


@router.delete("/{city}/sight/{sight}")
async def delete_sight(
    slug: str = Path(..., min_length=1),
    sight: str = Path(..., min_length=1),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_city),
):
    return {"hello here"}
