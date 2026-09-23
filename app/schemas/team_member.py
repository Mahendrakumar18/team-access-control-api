from pydantic import BaseModel


class TeamMemberCreate(BaseModel):
    user_id: int
    team_id: int
    role: str


class TeamMemberRoleUpdate(BaseModel):
    role: str