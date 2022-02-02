import uuid

from pydantic import BaseModel, Field


SIGHT_EXAMPLE = {
    "name": "Red Square",
    "location": ["55°45N", "37°37E"],
    "description": (
        "Red Square is the main square of Moscow and the most visited place in the capital of Russia."
        "The most famous Moscow sights, such as the Moscow Kremlin and St. Basil's Cathedral are located near Red Square."
        "The square is located in the city centre, along of the Kremlin eastern wall. Currently, it is a pedestrian area."
        "Red Square of Moscow is included in the UNESCO World Heritage Sites list."
    ),
    "visited": 10,
}

SIGHT_EXAMPLE_WITH_ID = SIGHT_EXAMPLE | {"id": "66a7d114-e178-4103-aac3-3e4ce0f56a2c"}

CITY_EXAMPLE = {
    "name": "Moscow",
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

CITY_EXAMPLE_WITH_ID = CITY_EXAMPLE | {"id": "ed3a8ab8-e9fe-472a-86c8-b4029de37e35"}


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


class DBModelMixin:
    id: str = Field(default_factory=uuid.uuid4, alias="_id")


class BaseSight(BaseModel):
    name: str = Field(...)
    locatoin: list[str, str] = Field(...)
    description: str = Field(...)
    visited: int = 0


class InputSight(BaseSight):
    class Config(InputSightConfig):
        pass


class FullSight(BaseSight, DBModelMixin):
    class Config(FullSightConfig):
        pass


class BaseCity(BaseModel):
    name: str = Field(...)
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


class FullCity(BaseCity, DBModelMixin):
    class Config(FullCityConfig):
        pass
