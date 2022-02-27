from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..crud.user import get_user_by_username

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api1/users/token")


def verify_password(password, hashed_password):
    return ctx.verify(password, hashed_password)


def get_password_hash(password):
    return ctx.hash(password)


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    additional = data.copy()
    expire = datetime.utcnow() + expires_delta
    additional["exp"] = expire
    return jwt.encode(additional, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(
    collection: AsyncIOMotorCollection, username: str, password: str
):
    user = await get_user_by_username(collection=collection, username=username)
    if user and user["active"] and verify_password(password, user["password"]):
        return user


async def get_current_user(collection: AsyncIOMotorCollection, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise CREDENTIALS_EXCEPTION
    except JWTError as e:
        raise CREDENTIALS_EXCEPTION from e
    user = await get_user_by_username(collection=collection, username=username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user
