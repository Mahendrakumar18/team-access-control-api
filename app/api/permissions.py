from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.team_member import TeamMember
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
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


@router.get("/check")
def check_permission(
    team_id: int,
    required_role: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id

    member = (
        db.query(TeamMember)
        .filter(
            TeamMember.user_id == user_id,
            TeamMember.team_id == team_id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=403,
            detail="User is not a member of this team"
        )

    actual_role = member.role.lower()
    required_role = required_role.lower()

    if actual_role not in ROLE_LEVELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown user role: {actual_role}"
        )

    if required_role not in ROLE_LEVELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown required role: {required_role}"
        )

    if ROLE_LEVELS[actual_role] < ROLE_LEVELS[required_role]:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied. User role is {actual_role}"
        )

    return {
        "allowed": True,
        "user_id": user_id,
        "team_id": team_id,
        "role": actual_role
    }