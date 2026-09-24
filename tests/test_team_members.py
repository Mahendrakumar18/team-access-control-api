from fastapi.testclient import TestClient

from app.main import app
from app.auth.security import hash_password
from app.models.user import User
from app.models.team import Team
from app.models.team_member import TeamMember
from tests.test_database import TestingSessionLocal


client = TestClient(app)


def setup_test_data():
    db = TestingSessionLocal()

    admin = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123")
    )

    member = User(
        name="Member User",
        email="member@example.com",
        hashed_password=hash_password("MemberPassword123")
    )

    team = Team(name="Test Team")

    db.add_all([admin, member, team])
    db.commit()

    db.refresh(admin)
    db.refresh(member)
    db.refresh(team)

    admin_membership = TeamMember(
        user_id=admin.id,
        team_id=team.id,
        role="admin"
    )

    member_membership = TeamMember(
        user_id=member.id,
        team_id=team.id,
        role="member"
    )

    db.add_all([admin_membership, member_membership])
    db.commit()

    db.refresh(member_membership)

    member_membership_id = member_membership.id

    db.close()

    return member_membership_id


def get_member_token():
    member_membership_id = setup_test_data()

    response = client.post(
        "/auth/login",
        json={
            "email": "member@example.com",
            "password": "MemberPassword123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"], member_membership_id


def test_member_cannot_add_team_member():
    token, member_membership_id = get_member_token()

    response = client.post(
        "/team-members/",
        json={
            "user_id": 1,
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
    token, member_membership_id = get_member_token()

    response = client.patch(
        f"/team-members/{member_membership_id}",
        json={"role": "admin"},
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_member_cannot_delete_team_member():
    token, member_membership_id = get_member_token()

    response = client.delete(
        f"/team-members/{member_membership_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"
    