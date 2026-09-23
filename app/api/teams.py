from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.schemas.team import TeamCreate


router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()


@router.post("/")
def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db)
):
    team = Team(
        name=team_data.name
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get("/{team_id}/members")
def get_team_members(
    team_id: int,
    db: Session = Depends(get_db)
):
    # Check if team exists
    team = (
        db.query(Team)
        .filter(Team.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    # Get all members of the team
    members = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id)
        .all()
    )

    return members 