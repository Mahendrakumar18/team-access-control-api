import os

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_member_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "newuser789@example.com",
            "password": os.getenv("TEST_MEMBER_PASSWORD")
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_member_cannot_add_team_member():
    token = get_member_token()

    response = client.post(
        "/team-members/",
        json={
            "user_id": 2,
            "team_id": 1,
            "role": "member"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_member_cannot_update_team_member_role():
    token = get_member_token()

    response = client.patch(
        "/team-members/3",
        json={
            "role": "admin"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_member_cannot_delete_team_member():
    token = get_member_token()

    response = client.delete(
        "/team-members/3",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"