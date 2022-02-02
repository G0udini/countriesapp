import uuid

from pydantic import BaseModel, Field
from bson import ObjectId

SIGHT_EXAMPLE = {
    "name": "Red Square",
    "slug": "red-square",
    "location": ["55°45N", "37°37E"],
    "description": (
        "Red Square is the main square of Moscow and the most visited place in the capital of Russia."
        "The most famous Moscow sights, such as the Moscow Kremlin and St. Basil's Cathedral are located near Red Square."
        "The square is located in the city centre, along of the Kremlin eastern wall. Currently, it is a pedestrian area."
        "Red Square of Moscow is included in the UNESCO World Heritage Sites list."
    ),
    "visited": 10,
}

SIGHT_EXAMPLE_WITH_ID = SIGHT_EXAMPLE | {"_id": "61f9a0a8485011106d5aa394"}

CITY_EXAMPLE = {
    "name": "Moscow",
    "slug": "moscow",
    "description": (
        "Moscow is the capital of Russia, its political, economic, and cultural centre."
        "This is the most populated city in Russia and Europe."
        "For many people from Russia and other countries the capital of Russia is a city of magnificent opportunities."
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

CITY_EXAMPLE_WITH_ID = CITY_EXAMPLE | {"_id": "61f9a0a8485011106d5aa394"}


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
    schema_extra = {"example": SIGHT_EXAMPLE_WITH_ID}


class BaseCityConfig:
    schema_extra = {"example": CITY_EXAMPLE}


class ViewCityConfig(BaseCityConfig):
    pass


class FullCityConfig(BaseCityConfig):
    allow_population_by_field_name = True
    schema_extra = {"example": CITY_EXAMPLE_WITH_ID}


class DBModelMixin(BaseModel):
    id: ObjectIdStr = Field(alias="_id")


class BaseSight(BaseModel):
    name: str = Field(...)
    slug: str
    locatoin: list[str, str] = Field(...)
    description: str = Field(...)
    visited: int = 0


class InputSight(BaseSight):
    class Config(InputSightConfig):
        pass


class FullSight(DBModelMixin, BaseSight):
    class Config(FullSightConfig):
        pass


class BaseCity(BaseModel):
    name: str = Field(...)
    slug: str
    description: str = Field(...)
    foundation_year: int | None = None
    time_zone: int | None = None
    square: float | None = None
    climate: str | None = None
    rating: float | None = None
    number_of_scores: int = 0
    sights: list[FullSight] = []
    reviews: list[str] = []


class ViewCity(BaseCity):
    class Config(ViewCityConfig):
        pass


class FullCity(DBModelMixin, BaseCity):
    class Config(FullCityConfig):
        pass
