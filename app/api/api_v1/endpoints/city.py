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

from ....db.base import AsyncIOMotorClient
from ....crud.city import (
    get_all_cities,
    insert_city_and_return,
    get_city_by_slug,
    update_city_and_return,
    delete_city_and_return,
    get_cities_by_rating,
)
from ....models.city import ViewCity, UpdateCity

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


async def get_mongodb_conn(request: Request) -> AsyncIOMotorClient:
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    return request.app.state.mongodb


@router.get(
    "/",
    response_model=list[ViewCity],
    response_description="List all cities",
)
async def list_all_cities(
    limit: int = Query(20, gt=0),
    skip: int = Query(0, ge=0),
    search: str = Query(None),
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    return await get_all_cities(conn=conn, limit=limit, skip=skip, search=search)


@router.post(
    "/",
    response_model=ViewCity,
    status_code=status.HTTP_201_CREATED,
    response_description="Add new city",
)
async def add_city(
    document: ViewCity = Body(...),
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    return await insert_city_and_return(conn=conn, document=document)


@router.get(
    "/{slug}/",
    response_model=ViewCity,
    response_description="Get city",
)
async def get_city(
    slug: str = Path(..., min_length=1),
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    city = await get_city_by_slug(conn=conn, slug=slug)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} not found"
        )
    return city


@router.put(
    "/{slug}/",
    response_model=ViewCity,
    response_description="Update city",
)
async def update_city(
    slug: str = Path(..., min_length=1),
    document: UpdateCity = Body(...),
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    city = await update_city_and_return(conn=conn, slug=slug, document=document)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} not found"
        )
    return city


@router.delete(
    "/{slug}/",
    response_model=ViewCity,
    response_description="Delete city",
)
async def delete_city(
    slug: str = Path(..., min_length=1),
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    city = await delete_city_and_return(conn=conn, slug=slug)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City {slug} not found"
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
    conn: AsyncIOMotorClient = Depends(get_mongodb_conn),
):
    return await get_cities_by_rating(conn=conn, limit=limit, skip=skip)
