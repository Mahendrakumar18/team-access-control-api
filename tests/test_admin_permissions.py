from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_admin_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "mahendra@example.com",
            "password": "Admin12345"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_admin_can_get_team_members():
    token = get_admin_token()

    response = client.get(
        "/team-members/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)