from pydantic import BaseModel, EmailStr
from .base import DBIdMixin

BASE_USER_EXAMPLE = {
    "username": "G0udini",
    "password": "123456",
}

REGISTER_USER_EXAMPLE = {"password2": "123456"} | BASE_USER_EXAMPLE

VIEW_USER_EXAMPLE = {
    "email": "ruslan@yandex.ru",
    "active": True,
    "staff": False,
    "visited_cities": [],
    "like_to_visit": [],
} | BASE_USER_EXAMPLE

FULL_USER_EXAMPLE = {"_id": "61f9a0a8485011106d5aa394"} | VIEW_USER_EXAMPLE


class BaseUserConfig:
    schema_extra = {"example": BASE_USER_EXAMPLE}


class LoginUserConfig(BaseUserConfig):
    pass


class RegisterUserConfig:
    schema_extra = {"example": REGISTER_USER_EXAMPLE}


class ViewUserConfig:
    schema_extra = {"example": VIEW_USER_EXAMPLE}


class FullUserConfig:
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_USER_EXAMPLE}


class BaseUser(BaseModel):
    username: str


class LoginUser(BaseUser):
    password: str

    class Config(LoginUserConfig):
        pass


class Register(LoginUser):
    password2: str

    class Config(RegisterUserConfig):
        pass


class ViewUser(BaseUser):
    email: EmailStr
    visited_cities: list[str]
    like_to_visit: list[str]

    class Config(ViewUserConfig):
        pass


class FullUser(DBIdMixin, ViewUser):
    active: bool = True
    staff: bool = False

    class Config(FullUserConfig):
        pass
