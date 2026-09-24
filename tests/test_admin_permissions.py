from fastapi.testclient import TestClient

from app.main import app
from app.auth.security import hash_password
from app.models.user import User
from app.models.team import Team
from app.models.team_member import TeamMember
from tests.test_database import TestingSessionLocal


client = TestClient(app)


def setup_admin():
    db = TestingSessionLocal()

    admin = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123")
    )

    team = Team(name="Admin Test Team")

    db.add_all([admin, team])
    db.commit()

    db.refresh(admin)
    db.refresh(team)

    membership = TeamMember(
        user_id=admin.id,
        team_id=team.id,
        role="admin"
    )

    db.add(membership)
    db.commit()

    db.close()


def get_admin_token():
    setup_admin()

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "AdminPassword123"
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
    
