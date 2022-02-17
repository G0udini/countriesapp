from app.models.sight import ViewSight


test_sight = {
    "name": "Bolshoi Theatre",
    "description": (
        "The Bolshoi Theater is home to the largest and one of the oldest ballet and "
        "opera companies in the world. While the theater has undergone several major "
        "renovations over the past century-including a recent one in 2011 to restore "
        "some of the imperial architectural details-it still retains all of "
        "its Neoclassical grandeur."
    ),
    "visited": 500,
    "rating": 4.5,
    "number_of_scores": 1200,
}
corrupted_test_sight = {
    "visited": 500,
    "rating": 4.5,
    "number_of_scores": 1200,
}

test_sight_slug = "bolshoi-theatre"


def test_list_all_sights(client):
    response = client.get("/api1/cities/moscow/sights")
    data = [ViewSight(**sight) for sight in response.json()]
    assert response.status_code == 200
    assert data[0].name == "Kremlin"
    assert data[1].name == "Museum of Cosmonautics"


def test_list_all_sights_with_query(client):
    response = client.get("/api1/cities/moscow/sights?skip=1&limit=1")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Museum of Cosmonautics"


def test_add_sight(client):
    response = client.post("/api1/cities/moscow/sights", json=test_sight)
    data = ViewSight(**response.json())
    assert response.status_code == 201
    assert data.name == test_sight["name"]


def test_list_sights_after_adding(client):
    response = client.get("/api1/cities/moscow/sights")
    data = [ViewSight(**sight) for sight in response.json()]
    assert response.status_code == 200
    assert data[0].name == "Kremlin"
    assert data[1].name == "Bolshoi Theatre"
    assert data[2].name == "Museum of Cosmonautics"


def test_add_duplicate_sight(client):
    response = client.post("/api1/cities/moscow/sights", json=test_sight)
    assert response.status_code == 409
    assert response.json()["detail"] == f"Sight '{test_sight['name']}' already exists"


def test_add_sight_without_required(client):
    response = client.post("/api1/cities/moscow/sights", json=corrupted_test_sight)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][1]["msg"] == "field required"


def test_get_sight(client):
    response = client.get(f"/api1/cities/moscow/sight/{test_sight_slug}")
    data = ViewSight(**response.json())
    assert response.status_code == 200
    assert data.name == test_sight["name"]


def test_get_nonexistent_sight(client):
    response = client.get("/api1/cities/moscow/sight/red-square")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sight 'red-square' was not found"


def test_update_sight(client):
    response = client.put(
        f"/api1/cities/moscow/sight/{test_sight_slug}", json={"visited": 600}
    )
    data = ViewSight(**response.json())
    assert response.status_code == 200
    assert data.name == test_sight["name"]
    assert data.visited == 600


def test_update_nonexistent_sight(client):
    response = client.put("/api1/cities/moscow/sight/red-square", json={"visited": 500})
    assert response.status_code == 404
    assert response.json()["detail"] == "Sight 'red-square' was not found"


def test_update_sight_to_already_existed(client):
    response = client.put(
        f"/api1/cities/moscow/sight/{test_sight_slug}",
        json={"name": "Museum of Cosmonautics"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Sight 'Museum of Cosmonautics' already exists"


def test_delete_sight(client):
    response = client.delete(f"/api1/cities/moscow/sight/{test_sight_slug}")
    data = ViewSight(**response.json())
    assert response.status_code == 200
    assert data.name == test_sight["name"]


def test_delete_nonexistent_sight(client):
    response = client.delete("/api1/cities/moscow/sight/WWW")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sight 'WWW' was not found"
