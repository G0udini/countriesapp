from pydantic import BaseModel, Field

from .base import DBModelMixin, DBRequiredNameMixin
from .sight import ViewSight

CITY_EXAMPLE = {
    "name": "Moscow",
    "description": (
        "Moscow is the capital of Russia, its political, economic, and cultural centre."
        "This is the most populated city in Russia and Europe."
        "For many people from Russia and other countries the capital of "
        "Russia is a city of magnificent opportunities."
    ),
    "foundation_year": 1147,
    "time_zone": 3,
    "square": 2561.5,
    "climate": "continental",
    "rating": 4.56,
    "number_of_scores": 3100,
    "sights": [],
    "reviews": [],
}

FULL_CITY_EXAMPLE = {
    "_id": "61f9a0a8485011106d5aa394",
    "slug": "moscow",
} | CITY_EXAMPLE


class BaseCityConfig:
    schema_extra = {"example": CITY_EXAMPLE}


class ViewCityConfig(BaseCityConfig):
    pass


class FullCityConfig:
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_CITY_EXAMPLE}


class BaseCity(BaseModel):
    name: str | None
    description: str | None
    foundation_year: int | None
    time_zone: int = 0
    square: float | None
    climate: str | None
    rating: float = Field(0, ge=0, le=5)
    number_of_scores: int = 0
    sights: list[ViewSight] = []
    reviews: list[str] = []


class ViewCity(DBRequiredNameMixin, BaseCity):
    class Config(ViewCityConfig):
        pass


class FullCity(DBRequiredNameMixin, DBModelMixin, BaseCity):
    class Config(FullCityConfig):
        pass


class UpdateCity(BaseCity):
    class Config(ViewCityConfig):
        pass
