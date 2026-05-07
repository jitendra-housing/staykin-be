from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.seeds.amenities import VALID_AMENITY_IDS
from app.db.seeds.bhks import VALID_BHK_IDS
from app.db.seeds.furnishings import VALID_FURNISHING_IDS
from app.db.seeds.listing_gender_prefs import VALID_LISTING_GENDER_PREF_IDS
from app.db.seeds.move_ins import VALID_MOVE_IN_IDS
from app.db.seeds.room_types import VALID_ROOM_TYPE_IDS
from app.schemas._validators import validate_id, validate_id_list


class ListingCreate(BaseModel):
    owner_user_id: int
    locality_id: int
    monthly_rent: int = Field(ge=0)
    bhk: int
    furnishing: int
    room_type: int
    flatmates_needed: int = Field(ge=1, le=5)
    gender_pref: int
    amenities: list[int] | None = None
    move_in: int
    photos: list[str] | None = None

    @field_validator("bhk")
    @classmethod
    def _vld_bhk(cls, v: int) -> int:
        return validate_id(v, VALID_BHK_IDS, "bhk")

    @field_validator("furnishing")
    @classmethod
    def _vld_furnishing(cls, v: int) -> int:
        return validate_id(v, VALID_FURNISHING_IDS, "furnishing")

    @field_validator("room_type")
    @classmethod
    def _vld_room_type(cls, v: int) -> int:
        return validate_id(v, VALID_ROOM_TYPE_IDS, "room_type")

    @field_validator("move_in")
    @classmethod
    def _vld_move_in(cls, v: int) -> int:
        return validate_id(v, VALID_MOVE_IN_IDS, "move_in")

    @field_validator("gender_pref")
    @classmethod
    def _vld_gender_pref(cls, v: int) -> int:
        return validate_id(v, VALID_LISTING_GENDER_PREF_IDS, "gender_pref")

    @field_validator("amenities")
    @classmethod
    def _vld_amenities(cls, v: list[int] | None) -> list[int] | None:
        return validate_id_list(v, VALID_AMENITY_IDS, "amenities")


class ListingUpdate(BaseModel):
    locality_id: int | None = None
    monthly_rent: int | None = Field(default=None, ge=0)
    bhk: int | None = None
    furnishing: int | None = None
    room_type: int | None = None
    flatmates_needed: int | None = Field(default=None, ge=1, le=5)
    gender_pref: int | None = None
    amenities: list[int] | None = None
    move_in: int | None = None
    photos: list[str] | None = None

    @field_validator("bhk")
    @classmethod
    def _vld_bhk(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_BHK_IDS, "bhk")

    @field_validator("furnishing")
    @classmethod
    def _vld_furnishing(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_FURNISHING_IDS, "furnishing")

    @field_validator("room_type")
    @classmethod
    def _vld_room_type(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_ROOM_TYPE_IDS, "room_type")

    @field_validator("move_in")
    @classmethod
    def _vld_move_in(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_MOVE_IN_IDS, "move_in")

    @field_validator("gender_pref")
    @classmethod
    def _vld_gender_pref(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_LISTING_GENDER_PREF_IDS, "gender_pref")

    @field_validator("amenities")
    @classmethod
    def _vld_amenities(cls, v: list[int] | None) -> list[int] | None:
        return validate_id_list(v, VALID_AMENITY_IDS, "amenities")


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_user_id: int
    locality_id: int
    monthly_rent: int
    bhk: int
    furnishing: int
    room_type: int
    flatmates_needed: int
    gender_pref: int
    amenities: list[int] | None
    move_in: int
    photos: list[str] | None
    created_at: datetime
    updated_at: datetime


class ListingFeedOut(ListingOut):
    total_residents: int
