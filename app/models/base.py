from bson import ObjectId
from pydantic import BaseModel, Field


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val):
        if not isinstance(val, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(val)


class DBModelMixin(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    slug: str


class DBRequiredNameMixin(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
