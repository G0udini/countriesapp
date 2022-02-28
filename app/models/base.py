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


class DBIdMixin(BaseModel):
    id: ObjectIdStr = Field(alias="_id")


class DBModelMixin(DBIdMixin, BaseModel):
    slug: str


class DBRequiredNameMixin(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class PasswordMixin(BaseModel):
    password: str
