from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)


def test_get_omcs():
    implemented = False
    assert implemented


def test_get_omcs_unauthorized():
    response = test_client.get("/omcs/")
    assert response.status_code == 401


def test_get_omcs_bad_token():
    response = test_client.get("/omcs/")
    assert response.status_code == 401
