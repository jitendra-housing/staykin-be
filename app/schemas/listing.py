from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    BHK,
    Amenity,
    Furnishing,
    ListingGenderPref,
    MoveIn,
)


class ListingCreate(BaseModel):
    owner_user_id: int
    locality_id: int
    monthly_rent: int = Field(ge=0)
    bhk: BHK
    furnishing: Furnishing
    flatmates_needed: int = Field(ge=1, le=20)
    gender_pref: ListingGenderPref
    amenities: list[Amenity] | None = None
    move_in: MoveIn
    photos: list[str] | None = None


class ListingUpdate(BaseModel):
    locality_id: int | None = None
    monthly_rent: int | None = Field(default=None, ge=0)
    bhk: BHK | None = None
    furnishing: Furnishing | None = None
    flatmates_needed: int | None = Field(default=None, ge=1, le=20)
    gender_pref: ListingGenderPref | None = None
    amenities: list[Amenity] | None = None
    move_in: MoveIn | None = None
    photos: list[str] | None = None


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_user_id: int
    locality_id: int
    monthly_rent: int
    bhk: BHK
    furnishing: Furnishing
    flatmates_needed: int
    gender_pref: ListingGenderPref
    amenities: list[Amenity] | None
    move_in: MoveIn
    photos: list[str] | None
    created_at: datetime
    updated_at: datetime
