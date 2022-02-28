from pydantic import BaseModel, EmailStr, validator
from .base import DBIdMixin, PasswordMixin


BASE_USER_EXAMPLE = {
    "username": "Ruslan",
}
LOGIN_USER_EXAMPLE = BASE_USER_EXAMPLE | {
    "password": "123456",
}

REGISTER_USER_EXAMPLE = {"password2": "123456"} | LOGIN_USER_EXAMPLE

UPDATE_USER_EXAMPLE = {
    "email": "ruslan@yandex.ru",
    "visited_cities": [],
    "like_to_visit": [],
}

VIEW_USER_EXAMPLE = BASE_USER_EXAMPLE | UPDATE_USER_EXAMPLE

FULL_USER_EXAMPLE = (
    LOGIN_USER_EXAMPLE
    | UPDATE_USER_EXAMPLE
    | {
        "active": True,
        "staff": False,
    }
)

FULL_DB_USER_EXAMPLE = {"_id": "61f9a0a8485011106d5aa394"} | FULL_USER_EXAMPLE


# Config Models
class LoginUserConfig:
    schema_extra = {"example": LOGIN_USER_EXAMPLE}


class RegisterUserConfig:
    schema_extra = {"example": REGISTER_USER_EXAMPLE}


class UpdateUserConfig:
    schema_extra = {"example": UPDATE_USER_EXAMPLE}


class ViewUserConfig:
    schema_extra = {"example": VIEW_USER_EXAMPLE}


class FullUserConfig:
    schema_extra = {"example": FULL_USER_EXAMPLE}


class FullDBUserConfig:
    allow_population_by_field_name = True
    schema_extra = {"example": FULL_DB_USER_EXAMPLE}


# User Models
class BaseUser(BaseModel):
    username: str

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class LoginUser(PasswordMixin, BaseUser):
    class Config(LoginUserConfig):
        pass


class RegisterUser(PasswordMixin, BaseUser):
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    class Config(RegisterUserConfig):
        pass


class UpdateUser(BaseModel):
    email: EmailStr = None
    visited_cities: list[str] = []
    like_to_visit: list[str] = []

    class Config(UpdateUserConfig):
        pass


class ViewUser(UpdateUser, BaseUser):
    class Config(ViewUserConfig):
        pass


class FullUser(UpdateUser, LoginUser):
    active: bool = True
    staff: bool = False

    class Config(FullUserConfig):
        pass


class FullDBUser(DBIdMixin, FullUser):
    class Config(FullDBUserConfig):
        pass
