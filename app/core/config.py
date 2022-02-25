import os

# Secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Database settings
DATABASE_URL = os.getenv("DB_URL", "")

if not DATABASE_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", 27017)
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "admin")
    MONGO_DB = os.getenv("MONGO_DB", "contries")

    DATABASE_URL = (
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )

DATABASE_NAME = os.getenv("MONGO_DB")

CITY_COLLECTION = "city"
CITY_TEST_COLLECTION = "test_city"

USER_COLLECTION = "user"
USER_TEST_COLLECTION = "test_user"
