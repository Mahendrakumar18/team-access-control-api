from fastapi import FastAPI

from app.db.database import engine, Base

from app.models.user import User
from app.models.team import Team
from app.models.team_member import TeamMember

from app.api.users import router as users_router
from app.api.teams import router as teams_router
from app.api.team_members import router as team_members_router
from app.api.permissions import router as permissions_router
from app.api.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users_router)
app.include_router(teams_router)
app.include_router(team_members_router)
app.include_router(permissions_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Team Access Control API is running"}