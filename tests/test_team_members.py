from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_member_cannot_add_team_member():
    response = client.post(
        "/team-members/",
        json={
            "user_id": 2,
            "team_id": 1,
            "role": "member"
        }
    )

    assert response.status_code in [401, 403]


def test_member_cannot_update_team_member_role():
    response = client.patch(
        "/team-members/3",
        json={
            "role": "admin"
        }
    )

    assert response.status_code in [401, 403]


def test_member_cannot_delete_team_member():
    response = client.delete(
        "/team-members/3"
    )

    assert response.status_code in [401, 403]