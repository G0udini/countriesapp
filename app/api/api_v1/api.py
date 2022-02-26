from fastapi import APIRouter

from .endpoints.city import router as city_router
from .endpoints.sight import router as sight_router
from .endpoints.user import router as user_router

router = APIRouter(
    prefix="/api1",
)
router.include_router(city_router)
router.include_router(sight_router)
router.include_router(user_router)
