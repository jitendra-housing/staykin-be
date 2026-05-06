from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.seeds.lifestyle_tags import (
    MAX_TAGS,
    MIN_TAGS,
    VALID_LIFESTYLE_TAG_IDS,
)
from app.models.enums import (
    BHK,
    Furnishing,
    Gender,
    MoveIn,
    RoomType,
)


def _validate_tag_ids(v: list[int] | None) -> list[int] | None:
    if v is None or len(v) == 0:
        return v
    if len(v) != len(set(v)):
        raise ValueError("lifestyle_tag_ids must be unique")
    invalid = sorted(set(v) - VALID_LIFESTYLE_TAG_IDS)
    if invalid:
        raise ValueError(f"unknown lifestyle_tag_ids: {invalid}")
    if not (MIN_TAGS <= len(v) <= MAX_TAGS):
        raise ValueError(f"select between {MIN_TAGS} and {MAX_TAGS} lifestyle tags")
    return v


class UserUpsert(BaseModel):
    phone: str = Field(min_length=7, max_length=20)
    name: str | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    gender: Gender | None = None
    occupation: str | None = None
    photo_url: str | None = None

    lifestyle_tag_ids: list[int] | None = None

    preferred_locality_ids: list[int] | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    bhk_prefs: list[BHK] | None = None
    room_type_pref: RoomType | None = None
    furnishing_prefs: list[Furnishing] | None = None
    move_in_pref: MoveIn | None = None
    move_in_date: date | None = None
    gender_pref: Gender | None = None

    @field_validator("lifestyle_tag_ids")
    @classmethod
    def _vld_tags(cls, v: list[int] | None) -> list[int] | None:
        return _validate_tag_ids(v)


class UserUpdate(UserUpsert):
    phone: str | None = Field(default=None, min_length=7, max_length=20)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str
    name: str | None
    age: int | None
    gender: Gender | None
    occupation: str | None
    photo_url: str | None

    lifestyle_tag_ids: list[int] | None

    preferred_locality_ids: list[int] | None
    budget_min: int | None
    budget_max: int | None
    bhk_prefs: list[BHK] | None
    room_type_pref: RoomType | None
    furnishing_prefs: list[Furnishing] | None
    move_in_pref: MoveIn | None
    move_in_date: date | None
    gender_pref: Gender | None

    created_at: datetime
    updated_at: datetime
