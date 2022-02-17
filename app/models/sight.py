from pydantic import BaseModel, Field

from .base import DBRequiredNameMixin


SIGHT_EXAMPLE = {
    "name": "Red Square",
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
    "rating": 3.8,
    "number_of_scores": 100,
}

FULL_SIGHT_EXAMPLE = {
    "slug": "red-square",
} | SIGHT_EXAMPLE


class BaseSightConfig:
    schema_extra = {"example": SIGHT_EXAMPLE}


class ViewSightConfig(BaseSightConfig):
    pass


class FullSightConfig:
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_SIGHT_EXAMPLE}


class BaseSight(BaseModel):
    name: str | None
    description: str | None
    visited: int = 0
    rating: float = Field(0, ge=0, le=5)
    number_of_scores: int = 0


class ViewSight(DBRequiredNameMixin, BaseSight):
    class Config(ViewSightConfig):
        pass


class FullSight(DBRequiredNameMixin, BaseSight):
    slug: str

    class Config(FullSightConfig):
        pass


class UpdateSight(BaseSight):
    class Config(ViewSightConfig):
        pass
