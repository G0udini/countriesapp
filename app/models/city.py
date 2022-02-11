import uuid

from pydantic import BaseModel, Field
from bson import ObjectId

SIGHT_EXAMPLE = {
    "name": "Red Square",
    "location": ["55°45N", "37°37E"],
    "description": (
        "Red Square is the main square of Moscow and the most visited "
        "place in the capital of Russia."
        "The most famous Moscow sights, such as the Moscow Kremlin and "
        "St. Basil's Cathedral are located near Red Square."
        "The square is located in the city centre, along of the Kremlin eastern wall. "
        "Currently, it is a pedestrian area."
        "Red Square of Moscow is included in the UNESCO World Heritage Sites list."
    ),
    "visited": 10,
}

FULL_SIGHT_EXAMPLE = {
    "_id": "61f9a0a8485011106d5aa394",
    "slug": "red-square",
} | SIGHT_EXAMPLE

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


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val):
        if not isinstance(val, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(val)


class BaseSightConfig:
    schema_extra = {"example": SIGHT_EXAMPLE}


class InputSightConfig(BaseSightConfig):
    pass


class FullSightConfig(BaseSightConfig):
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_SIGHT_EXAMPLE}


class BaseCityConfig:
    schema_extra = {"example": CITY_EXAMPLE}


class ViewCityConfig(BaseCityConfig):
    pass


class FullCityConfig(BaseCityConfig):
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_CITY_EXAMPLE}


class DBModelMixin(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    slug: str


class DBRequiredMixin(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class BaseSight(BaseModel):
    name: str | None
    description: str | None
    locatoin: list[str, str] | None
    visited: int = 0


class InputSight(DBRequiredMixin, BaseSight):
    class Config(InputSightConfig):
        pass


class FullSight(DBRequiredMixin, DBModelMixin, BaseSight):
    class Config(FullSightConfig):
        pass


class BaseCity(BaseModel):
    name: str | None
    description: str | None
    foundation_year: int | None
    time_zone: int = 0
    square: float | None
    climate: str | None
    rating: float = Field(0, ge=0, le=5)
    number_of_scores: int = 0
    sights: list[FullSight] = []
    reviews: list[str] = []


class ViewCity(DBRequiredMixin, BaseCity):
    class Config(ViewCityConfig):
        pass


class FullCity(DBRequiredMixin, DBModelMixin, BaseCity):
    class Config(FullCityConfig):
        pass


class UpdateCity(BaseCity):
    class Config(ViewCityConfig):
        pass
