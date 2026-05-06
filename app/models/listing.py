from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.enums import (
    BHK,
    Amenity,
    Furnishing,
    ListingGenderPref,
    MoveIn,
)


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    locality_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"), nullable=False, index=True
    )

    monthly_rent: Mapped[int] = mapped_column(Integer, nullable=False)
    bhk: Mapped[BHK] = mapped_column(Enum(BHK, name="bhk", create_type=False), nullable=False)
    furnishing: Mapped[Furnishing] = mapped_column(
        Enum(Furnishing, name="furnishing", create_type=False), nullable=False
    )
    flatmates_needed: Mapped[int] = mapped_column(Integer, nullable=False)
    gender_pref: Mapped[ListingGenderPref] = mapped_column(
        Enum(ListingGenderPref, name="listing_gender_pref"), nullable=False
    )
    amenities: Mapped[list[Amenity] | None] = mapped_column(
        ARRAY(PgEnum(Amenity, name="amenity", create_type=False))
    )
    move_in: Mapped[MoveIn] = mapped_column(
        Enum(MoveIn, name="move_in", create_type=False), nullable=False
    )
    photos: Mapped[list[str] | None] = mapped_column(ARRAY(String(512)))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
