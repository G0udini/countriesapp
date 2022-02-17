from pydantic import BaseModel


REVIEW_EXAMPLE = {
    "username": "G0udini",
    "description": "This is the most beautiful city I have ever seen",
    "rating": 4.9,
}


class ViewReview(BaseModel):
    username: str
    description: str
    rating: float

    class Config:
        schema_extra = {"example": REVIEW_EXAMPLE}
