from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.team_member import TeamMember
from app.models.user import User
from app.models.team import Team
from app.schemas.team_member import (
    TeamMemberCreate,
    TeamMemberRoleUpdate
)
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/team-members",
    tags=["Team Members"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ROLE_LEVELS = {
    "viewer": 1,
    "member": 2,
    "manager": 3,
    "admin": 4
}


def check_admin_access(
    current_user,
    team_id: int,
    db: Session
):
    admin_member = (
        db.query(TeamMember)
        .filter(
            TeamMember.user_id == current_user.id,
            TeamMember.team_id == team_id
        )
        .first()
    )

    if not admin_member or admin_member.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


@router.post("/")
def add_team_member(
    member_data: TeamMemberCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_admin_access(
        current_user,
        member_data.team_id,
        db
    )

    user = (
        db.query(User)
        .filter(User.id == member_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    team = (
        db.query(Team)
        .filter(Team.id == member_data.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    existing_member = (
        db.query(TeamMember)
        .filter(
            TeamMember.user_id == member_data.user_id,
            TeamMember.team_id == member_data.team_id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this team"
        )

    member = TeamMember(
        user_id=member_data.user_id,
        team_id=member_data.team_id,
        role=member_data.role
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get("/")
def get_team_members(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(TeamMember).all()


@router.delete("/{membership_id}")
def delete_team_member(
    membership_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = (
        db.query(TeamMember)
        .filter(TeamMember.id == membership_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team membership not found"
        )

    check_admin_access(
        current_user,
        member.team_id,
        db
    )

    db.delete(member)
    db.commit()

    return {
        "message": "Team membership deleted successfully"
    }


@router.patch("/{membership_id}")
def update_team_member_role(
    membership_id: int,
    role_data: TeamMemberRoleUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = (
        db.query(TeamMember)
        .filter(TeamMember.id == membership_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team membership not found"
        )

    check_admin_access(
        current_user,
        member.team_id,
        db
    )

    new_role = role_data.role.lower()

    if new_role not in ROLE_LEVELS:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Use viewer, member, manager, or admin"
        )

    member.role = new_role

    db.commit()
    db.refresh(member)

    return member