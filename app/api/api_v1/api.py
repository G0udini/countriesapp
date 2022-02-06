from fastapi import APIRouter

from .endpoints.city import router as city_router

router = APIRouter(
    prefix="/api1",
)
router.include_router(city_router)
