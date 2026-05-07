from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    owner_user_id: int
    member_user_id: int
    name: str | None = None


class TeamMemberAdd(BaseModel):
    user_id: int


class TeamMemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    joined_at: datetime


class TeamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_user_id: int
    name: str | None
    created_at: datetime
    updated_at: datetime


class TeamDetailOut(TeamOut):
    members: list[TeamMemberOut]
