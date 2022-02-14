from app.models.city import ViewCity

test_city = {
    "name": "Tomsk",
    "description": (
        "Moscow is the capital of Russia, its political, "
        "economic, and cultural centre."
        "This is the most populated city in Russia and Europe."
        "For many people from Russia and other countries the capital of Russia "
        "is a city of magnificent opportunities."
    ),
    "foundation_year": 1147,
    "time_zone": 3,
    "square": 2561.5,
    "climate": "continental",
    "rating": 4.56,
    "number_of_scores": 3100,
    "sights": [],
    "reviews": [],
}
corrupted_test_city = {
    "time_zone": 3,
    "square": 2561.5,
    "climate": "continental",
}

test_city_slug = "tomsk"


def test_list_all_cities(client):
    response = client.get("/api1/cities/")
    data = [ViewCity(**city) for city in response.json()]
    assert response.status_code == 200
    assert data[0].name == "Moscow"
    assert data[1].name == "Saint-Petersburg"


def test_list_all_cities_with_query(client):
    response = client.get("/api1/cities?search=moscow&skip=0&limit=20")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Moscow"


def test_add_city(client):
    response = client.post("/api1/cities/", json=test_city)
    data = ViewCity(**response.json())
    assert response.status_code == 201
    assert data.name == test_city["name"]


def test_add_duplicate_city(client):
    response = client.post("/api1/cities/", json=test_city)
    assert response.status_code == 409
    assert response.json()["detail"] == f"City '{test_city['name']}' already exists"


def test_add_city_without_required(client):
    response = client.post("/api1/cities/", json=corrupted_test_city)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][1]["msg"] == "field required"


def test_get_city(client):
    response = client.get(f"/api1/cities/{test_city_slug}")
    data = ViewCity(**response.json())
    assert response.status_code == 200
    assert data.name == test_city["name"]


def test_get_nonexistent_city(client):
    response = client.get("/api1/cities/mmoscow")
    assert response.status_code == 404
    assert response.json()["detail"] == "City mmoscow was not found"


def test_update_city(client):
    response = client.put(f"/api1/cities/{test_city_slug}", json={"time_zone": 5})
    data = ViewCity(**response.json())
    assert response.status_code == 200
    assert data.name == test_city["name"]
    assert data.time_zone == 5


def test_update_nonexistent_city(client):
    response = client.put("/api1/cities/mmoscow", json={"time_zone": 5})
    assert response.status_code == 404
    assert response.json()["detail"] == "City mmoscow was not found"


def test_delete_city(client):
    response = client.delete(f"/api1/cities/{test_city_slug}")
    data = ViewCity(**response.json())
    assert response.status_code == 200
    assert data.name == test_city["name"]


def test_delete_nonexistent_city(client):
    response = client.delete("/api1/cities/mmoscow")
    assert response.status_code == 404
    assert response.json()["detail"] == "City mmoscow was not found"


def test_get_city_rating(client):
    response = client.get("/api1/cities/top/")
    data = [ViewCity(**city) for city in response.json()]
    assert response.status_code == 200
    assert data[0].name == "Saint-Petersburg"
    assert data[1].name == "Moscow"
