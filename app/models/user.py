from datetime import date, datetime

from sqlalchemy import ARRAY, Date, DateTime, Enum, Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.enums import (
    BHK,
    Furnishing,
    Gender,
    MoveIn,
    RoomType,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    name: Mapped[str | None] = mapped_column(String(120))
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[Gender | None] = mapped_column(Enum(Gender, name="gender"))
    occupation: Mapped[str | None] = mapped_column(String(120))
    photo_url: Mapped[str | None] = mapped_column(String(512))

    # Lifestyle: ids reference the static LIFESTYLE_TAGS constant (5–10 enforced in schema).
    lifestyle_tag_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))

    # Search prefs
    preferred_locality_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    budget_min: Mapped[int | None] = mapped_column(Integer)
    budget_max: Mapped[int | None] = mapped_column(Integer)
    bhk_prefs: Mapped[list[BHK] | None] = mapped_column(
        ARRAY(PgEnum(BHK, name="bhk", create_type=False))
    )
    room_type_pref: Mapped[RoomType | None] = mapped_column(Enum(RoomType, name="room_type"))
    furnishing_prefs: Mapped[list[Furnishing] | None] = mapped_column(
        ARRAY(PgEnum(Furnishing, name="furnishing", create_type=False))
    )
    move_in_pref: Mapped[MoveIn | None] = mapped_column(Enum(MoveIn, name="move_in"))
    move_in_date: Mapped[date | None] = mapped_column(Date)
    gender_pref: Mapped[Gender | None] = mapped_column(Enum(Gender, name="gender_pref"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
