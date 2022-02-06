from fastapi.testclient import TestClient

from .app.main import app


client = TestClient(app)


def test_list_all_cities():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {}