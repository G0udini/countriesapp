from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from ....core.security import authenticate_user, create_access_token, get_password_hash
from ....db.dependencies import (
    get_current_active_user,
    get_mongodb_conn_for_user,
)
from ....models.token import Token
from ....models.user import ViewUser, RegisterUser
from ....crud.user import create_user
from ....models.shortcuts import (
    ADDITIONAL_CONFLICT_USER_SCHEMA,
    ADDITIONAL_UNAUTHORIZED_SCHEMA,
    ADDITIONAL_SUCCESSFUL_CREATED_USER_SCHEMA,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/token",
    response_model=Token,
    response_description="Get token",
    responses=ADDITIONAL_UNAUTHORIZED_SCHEMA,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_user),
):
    user = await authenticate_user(
        collection=collection, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    response_description="Register user",
    responses={
        **ADDITIONAL_CONFLICT_USER_SCHEMA,
        **ADDITIONAL_SUCCESSFUL_CREATED_USER_SCHEMA,
    },
)
async def register_user(
    form: RegisterUser = Body(...),
    collection: AsyncIOMotorCollection = Depends(get_mongodb_conn_for_user),
):
    form.password = get_password_hash(form.password)
    try:
        await create_user(collection=collection, form=form)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User '{form.username}' already exists",
        ) from e
    return {"detail": "User successfully created"}


@router.get("/users/me/", response_model=ViewUser)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
