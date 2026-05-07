from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.db.seeds.decision_statuses import VALID_DECISION_STATUS_IDS
from app.db.seeds.request_statuses import VALID_REQUEST_STATUS_IDS
from app.db.seeds.request_target_kinds import VALID_REQUEST_TARGET_KIND_IDS
from app.schemas._validators import validate_id


class RequestCreate(BaseModel):
    from_user_id: int
    target_kind: int
    target_id: int

    @field_validator("target_kind")
    @classmethod
    def _vld_target_kind(cls, v: int) -> int:
        return validate_id(v, VALID_REQUEST_TARGET_KIND_IDS, "target_kind")


class RequestDecisionAction(BaseModel):
    user_id: int


class RequestDecisionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    decision: int
    decided_at: datetime | None

    @field_validator("decision")
    @classmethod
    def _vld_decision(cls, v: int) -> int:
        return validate_id(v, VALID_DECISION_STATUS_IDS, "decision")


class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_user_id: int
    target_kind: int
    target_user_id: int | None
    target_team_id: int | None
    status: int
    decided_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @field_validator("target_kind")
    @classmethod
    def _vld_target_kind(cls, v: int) -> int:
        return validate_id(v, VALID_REQUEST_TARGET_KIND_IDS, "target_kind")

    @field_validator("status")
    @classmethod
    def _vld_status(cls, v: int) -> int:
        return validate_id(v, VALID_REQUEST_STATUS_IDS, "status")


class RequestDetailOut(RequestOut):
    decisions: list[RequestDecisionOut]
    room_id: int | None = None
