from datetime import date, datetime

from sqlalchemy import ARRAY, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    name: Mapped[str | None] = mapped_column(String(120))
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[int | None] = mapped_column(Integer)
    occupation: Mapped[int | None] = mapped_column(Integer)
    photo_url: Mapped[str | None] = mapped_column(String(512))

    # Lifestyle: ids reference LIFESTYLE_TAGS (5–10 enforced in schema).
    lifestyle_tag_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))

    # Search prefs (all id-based against constants in app/db/seeds/).
    preferred_locality_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    budget_min: Mapped[int | None] = mapped_column(Integer)
    budget_max: Mapped[int | None] = mapped_column(Integer)
    bhk_prefs: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    room_type_pref: Mapped[int | None] = mapped_column(Integer)
    furnishing_prefs: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    move_in_pref: Mapped[int | None] = mapped_column(Integer)
    move_in_date: Mapped[date | None] = mapped_column(Date)
    gender_pref: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
