import os


SECRET_KEY = os.getenv("SECRET_KEY")

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
