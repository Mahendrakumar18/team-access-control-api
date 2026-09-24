from fastapi.testclient import TestClient

from app.main import app
from tests.test_database import TestingSessionLocal
from app.models.user import User
from app.auth.security import hash_password


client = TestClient(app)


def test_register_missing_fields():
    response = client.post("/auth/register", json={})

    assert response.status_code == 422


def test_login_missing_fields():
    response = client.post("/auth/login", json={})

    assert response.status_code == 422


def test_login_invalid_credentials():
    db = TestingSessionLocal()

    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password=hash_password("CorrectPassword123")
    )

    db.add(user)
    db.commit()
    db.close()

    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "WrongPassword123"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    