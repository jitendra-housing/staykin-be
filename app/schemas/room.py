from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoomParticipantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    joined_at: datetime


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    flatmate_team_id: int | None
    add_flatmate_enabled: bool
    created_at: datetime


class RoomDetailOut(RoomOut):
    participants: list[RoomParticipantOut]


class AddFlatmateAction(BaseModel):
    user_id: int
