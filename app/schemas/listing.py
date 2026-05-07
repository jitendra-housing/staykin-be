from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.seeds.bhks import VALID_BHK_IDS
from app.db.seeds.furnishings import VALID_FURNISHING_IDS
from app.db.seeds.listing_gender_prefs import VALID_LISTING_GENDER_PREF_IDS
from app.db.seeds.move_ins import VALID_MOVE_IN_IDS
from app.models.enums import Amenity
from app.schemas._validators import validate_id


class ListingCreate(BaseModel):
    owner_user_id: int
    locality_id: int
    monthly_rent: int = Field(ge=0)
    bhk: int
    furnishing: int
    flatmates_needed: int = Field(ge=1, le=20)
    gender_pref: int
    amenities: list[Amenity] | None = None
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

    @field_validator("move_in")
    @classmethod
    def _vld_move_in(cls, v: int) -> int:
        return validate_id(v, VALID_MOVE_IN_IDS, "move_in")

    @field_validator("gender_pref")
    @classmethod
    def _vld_gender_pref(cls, v: int) -> int:
        return validate_id(v, VALID_LISTING_GENDER_PREF_IDS, "gender_pref")


class ListingUpdate(BaseModel):
    locality_id: int | None = None
    monthly_rent: int | None = Field(default=None, ge=0)
    bhk: int | None = None
    furnishing: int | None = None
    flatmates_needed: int | None = Field(default=None, ge=1, le=20)
    gender_pref: int | None = None
    amenities: list[Amenity] | None = None
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

    @field_validator("move_in")
    @classmethod
    def _vld_move_in(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_MOVE_IN_IDS, "move_in")

    @field_validator("gender_pref")
    @classmethod
    def _vld_gender_pref(cls, v: int | None) -> int | None:
        return validate_id(v, VALID_LISTING_GENDER_PREF_IDS, "gender_pref")


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_user_id: int
    locality_id: int
    monthly_rent: int
    bhk: int
    furnishing: int
    flatmates_needed: int
    gender_pref: int
    amenities: list[Amenity] | None
    move_in: int
    photos: list[str] | None
    created_at: datetime
    updated_at: datetime
