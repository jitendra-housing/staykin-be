from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.seeds.bhks import VALID_BHK_IDS
from app.db.seeds.furnishings import VALID_FURNISHING_IDS
from app.db.seeds.genders import VALID_GENDER_IDS
from app.db.seeds.lifestyle_tags import (
    MAX_TAGS,
    MIN_TAGS,
    VALID_LIFESTYLE_TAG_IDS,
)
from app.db.seeds.move_ins import VALID_MOVE_IN_IDS
from app.db.seeds.occupations import VALID_OCCUPATION_IDS
from app.db.seeds.room_types import VALID_ROOM_TYPE_IDS
from app.schemas._validators import validate_id, validate_id_list


class UserUpsert(BaseModel):
    phone: str = Field(min_length=7, max_length=20)
    name: str | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    gender: int | None = None
    occupation: int | None = None
    photo_url: str | None = None

    lifestyle_tag_ids: list[int] | None = None

    preferred_locality_ids: list[int] | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    bhk_prefs: list[int] | None = None
    room_type_pref: int | None = None
    furnishing_prefs: list[int] | None = None
    move_in_pref: int | None = None
    move_in_date: date | None = None
    gender_pref: int | None = None

    @field_validator("gender")
    @classmethod
    def _vld_gender(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_GENDER_IDS, "gender")

    @field_validator("occupation")
    @classmethod
    def _vld_occupation(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_OCCUPATION_IDS, "occupation")

    @field_validator("gender_pref")
    @classmethod
    def _vld_gender_pref(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_GENDER_IDS, "gender_pref")

    @field_validator("room_type_pref")
    @classmethod
    def _vld_room_type(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_ROOM_TYPE_IDS, "room_type_pref")

    @field_validator("move_in_pref")
    @classmethod
    def _vld_move_in(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_MOVE_IN_IDS, "move_in_pref")

    @field_validator("bhk_prefs")
    @classmethod
    def _vld_bhks(cls, v: list[int] | None) -> list[int] | None:
        return validate_id_list(v, VALID_BHK_IDS, "bhk_prefs")

    @field_validator("furnishing_prefs")
    @classmethod
    def _vld_furnishings(cls, v: list[int] | None) -> list[int] | None:
        return validate_id_list(v, VALID_FURNISHING_IDS, "furnishing_prefs")

    @field_validator("lifestyle_tag_ids")
    @classmethod
    def _vld_tags(cls, v: list[int] | None) -> list[int] | None:
        return validate_id_list(
            v, VALID_LIFESTYLE_TAG_IDS, "lifestyle_tag_ids", MIN_TAGS, MAX_TAGS
        )


class UserUpdate(UserUpsert):
    phone: str | None = Field(default=None, min_length=7, max_length=20)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str
    name: str | None
    age: int | None
    gender: int | None
    occupation: int | None
    photo_url: str | None

    lifestyle_tag_ids: list[int] | None

    preferred_locality_ids: list[int] | None
    budget_min: int | None
    budget_max: int | None
    bhk_prefs: list[int] | None
    room_type_pref: int | None
    furnishing_prefs: list[int] | None
    move_in_pref: int | None
    move_in_date: date | None
    gender_pref: int | None

    listing_ids: list[int] = []
    team_member_ids: list[int] = []

    vibe_score: int | None = None

    created_at: datetime
    updated_at: datetime
