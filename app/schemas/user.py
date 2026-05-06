from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    BHK,
    Cleanliness,
    FoodPref,
    Frequency,
    Furnishing,
    Gender,
    MoveIn,
    RoomType,
    SleepSchedule,
    YesNoSometimes,
)


class UserUpsert(BaseModel):
    phone: str = Field(min_length=7, max_length=20)
    name: str | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    gender: Gender | None = None
    occupation: str | None = None
    photo_url: str | None = None

    sleep_schedule: SleepSchedule | None = None
    cleanliness: Cleanliness | None = None
    smoking: YesNoSometimes | None = None
    drinking: YesNoSometimes | None = None
    food_pref: FoodPref | None = None
    pets: YesNoSometimes | None = None
    guests_frequency: Frequency | None = None
    work_from_home: Frequency | None = None
    noise_tolerance: Frequency | None = None
    languages: list[str] | None = None

    preferred_locality_ids: list[int] | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    bhk_prefs: list[BHK] | None = None
    room_type_pref: RoomType | None = None
    furnishing_prefs: list[Furnishing] | None = None
    move_in_pref: MoveIn | None = None
    move_in_date: date | None = None
    gender_pref: Gender | None = None


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

    sleep_schedule: SleepSchedule | None
    cleanliness: Cleanliness | None
    smoking: YesNoSometimes | None
    drinking: YesNoSometimes | None
    food_pref: FoodPref | None
    pets: YesNoSometimes | None
    guests_frequency: Frequency | None
    work_from_home: Frequency | None
    noise_tolerance: Frequency | None
    languages: list[str] | None

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
