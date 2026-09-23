from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_missing_fields():
    response = client.post(
        "/auth/register",
        json={}
    )

    assert response.status_code == 422


def test_login_missing_fields():
    response = client.post(
        "/auth/login",
        json={}
    )

    assert response.status_code == 422


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"