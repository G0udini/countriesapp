from fastapi import Request
from fastapi.testclient import TestClient

from app.main import app
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.config import CITY_TEST_COLLECTION
from app.api.api_v1.endpoints.city import get_mongodb_conn_for_city
from app.models.city import ViewCity


test_city = {
    "name": "Tomsk",
    "description": "Moscow is the capital of Russia, its political, economic, and cultural centre.This is the most populated city in Russia and Europe.For many people from Russia and other countries the capital of Russia is a city of magnificent opportunities.",
    "foundation_year": 1147,
    "time_zone": 3,
    "square": 2561.5,
    "climate": "continental",
    "rating": 4.56,
    "number_of_scores": 3100,
    "sights": [],
    "reviews": [],
}
test_city_slug = "tomsk"


async def get_test_mongodb_conn_for_city(request: Request) -> AsyncIOMotorCollection:
    if not hasattr(request.app.state, "mongodb"):
        raise AttributeError("mongodb attribute not set on app state")
    if not hasattr(request.app.state.mongodb, CITY_TEST_COLLECTION):
        raise AttributeError("mongodb client not set on app state")
    return request.app.state.mongodb[CITY_TEST_COLLECTION]


app.dependency_overrides[get_mongodb_conn_for_city] = get_test_mongodb_conn_for_city


def test_list_all_cities():
    with TestClient(app) as client:
        response = client.get("/api1/cities/")
        data = [ViewCity(**city) for city in response.json()]
        assert response.status_code == 200
        assert data[0].name == "Moscow"
        assert data[1].name == "Saint-Petersburg"


def test_list_all_cities_with_query():
    with TestClient(app) as client:
        response = client.get("/api1/cities?search=moscow&skip=0&limit=20")
        assert response.status_code == 200
        assert response.json()[0]["name"] == "Moscow"


def test_add_city():
    with TestClient(app) as client:
        response = client.post("/api1/cities/", json=test_city)
        data = ViewCity(**response.json())
        assert response.status_code == 201
        assert data.name == test_city["name"]


def test_add_duplicate_city():
    with TestClient(app) as client:
        response = client.post("/api1/cities/", json=test_city)
        assert response.status_code == 409
        assert response.json()["detail"] == f"City '{test_city['name']}' already exists"


def test_get_city():
    with TestClient(app) as client:
        response = client.get(f"/api1/cities/{test_city_slug}")
        data = ViewCity(**response.json())
        assert response.status_code == 200
        assert data.name == test_city["name"]


def test_get_nonexistent_city():
    with TestClient(app) as client:
        response = client.get("/api1/cities/mmoscow")
        assert response.status_code == 404
        assert response.json()["detail"] == "City mmoscow not found"


def test_update_city():
    with TestClient(app) as client:
        response = client.put(f"/api1/cities/{test_city_slug}", json={"time_zone": 5})
        data = ViewCity(**response.json())
        assert response.status_code == 200
        assert data.name == test_city["name"]
        assert data.time_zone == 5


def test_update_nonexistent_city():
    with TestClient(app) as client:
        response = client.put("/api1/cities/mmoscow", json={"time_zone": 5})
        assert response.status_code == 404
        assert response.json()["detail"] == "City mmoscow not found"


def test_delete_city():
    with TestClient(app) as client:
        response = client.delete(f"/api1/cities/{test_city_slug}")
        data = ViewCity(**response.json())
        assert response.status_code == 200
        assert data.name == test_city["name"]


def test_delete_nonexistent_city():
    with TestClient(app) as client:
        response = client.delete("/api1/cities/mmoscow")
        assert response.status_code == 404
        assert response.json()["detail"] == "City mmoscow not found"


def test_get_city_rating():
    with TestClient(app) as client:
        response = client.get("/api1/cities/top/")
        data = [ViewCity(**city) for city in response.json()]
        assert response.status_code == 200
        assert data[0].name == "Saint-Petersburg"
        assert data[1].name == "Moscow"
