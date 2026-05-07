from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import DecisionStatus, RequestStatus, RequestTargetKind


class RequestCreate(BaseModel):
    from_user_id: int
    target_kind: RequestTargetKind
    target_id: int


class RequestDecisionAction(BaseModel):
    user_id: int


class RequestDecisionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    decision: DecisionStatus
    decided_at: datetime | None


class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_user_id: int
    target_kind: RequestTargetKind
    target_user_id: int | None
    target_team_id: int | None
    status: RequestStatus
    decided_at: datetime | None
    created_at: datetime
    updated_at: datetime


class RequestDetailOut(RequestOut):
    decisions: list[RequestDecisionOut]
