from pydantic import BaseModel, EmailStr, validator
from .base import DBIdMixin

BASE_USER_EXAMPLE = {
    "username": "G0udini",
    "password": "123456",
}

REGISTER_USER_EXAMPLE = {"password2": "123456"} | BASE_USER_EXAMPLE

VIEW_USER_EXAMPLE = {
    "email": "ruslan@yandex.ru",
    "visited_cities": [],
    "like_to_visit": [],
}

FULL_USER_EXAMPLE = {
    "active": True,
    "staff": False,
} | VIEW_USER_EXAMPLE


FULL_DB_USER_EXAMPLE = {"_id": "61f9a0a8485011106d5aa394"} | FULL_USER_EXAMPLE


class BaseUserConfig:
    schema_extra = {"example": BASE_USER_EXAMPLE}


class LoginUserConfig(BaseUserConfig):
    pass


class RegisterUserConfig:
    schema_extra = {"example": REGISTER_USER_EXAMPLE}


class ViewUserConfig:
    schema_extra = {"example": VIEW_USER_EXAMPLE}


class FullUserConfig:
    schema_extra = {"example": FULL_USER_EXAMPLE}


class FullDBUserConfig:
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_DB_USER_EXAMPLE}


class BaseUser(BaseModel):
    username: str

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class LoginUser(BaseUser):
    password: str

    class Config(LoginUserConfig):
        pass


class RegisterUser(LoginUser):
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    class Config(RegisterUserConfig):
        pass


class ViewUser(BaseUser):
    email: EmailStr = None
    visited_cities: list[str] = []
    like_to_visit: list[str] = []

    class Config(ViewUserConfig):
        pass


class FullUser(LoginUser, ViewUser):
    active: bool = True
    staff: bool = False

    class Config(FullUserConfig):
        pass


class FullDBUser(DBIdMixin, FullUser):
    class Config(FullDBUserConfig):
        pass
