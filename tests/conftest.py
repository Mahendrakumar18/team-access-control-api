import pytest

from app.main import app
from app.db.database import Base

from app.api.auth import get_db as auth_get_db
from app.auth.dependencies import get_db as dependency_get_db
from app.api.team_members import get_db as team_members_get_db

from tests.test_database import engine, TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[auth_get_db] = override_get_db
app.dependency_overrides[dependency_get_db] = override_get_db
app.dependency_overrides[team_members_get_db] = override_get_db
