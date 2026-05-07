from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.enums import DecisionStatus, RequestStatus, RequestTargetKind


class ConnectionRequest(Base):
    __tablename__ = "requests"
    __table_args__ = (
        CheckConstraint(
            "(target_kind = 'USER' AND target_user_id IS NOT NULL AND target_team_id IS NULL)"
            " OR (target_kind = 'TEAM' AND target_team_id IS NOT NULL AND target_user_id IS NULL)",
            name="ck_requests_target_consistency",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    from_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_kind: Mapped[RequestTargetKind] = mapped_column(
        Enum(RequestTargetKind, name="request_target_kind"), nullable=False
    )
    target_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    target_team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=True, index=True
    )
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status"), nullable=False
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class ConnectionRequestDecision(Base):
    __tablename__ = "request_decisions"

    request_id: Mapped[int] = mapped_column(
        ForeignKey("requests.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    decision: Mapped[DecisionStatus] = mapped_column(
        Enum(DecisionStatus, name="decision_status"), nullable=False
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
