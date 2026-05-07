"""initial schema: users, localities, listings, teams, requests, rooms.

All categorical fields are integer ids referencing the constants in
app/db/seeds/. No Postgres ENUM types.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.db.seeds.localities import LOCALITIES

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── Localities ─────────────────────────────────────────────────────────
    op.create_table(
        "localities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.bulk_insert(
        sa.table(
            "localities",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [{"id": _id, "name": name} for _id, name in LOCALITIES],
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('localities', 'id'), "
        "(SELECT MAX(id) FROM localities))"
    )

    # ── Users ──────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("phone", sa.String(length=20), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.Integer(), nullable=True),
        sa.Column("occupation", sa.Integer(), nullable=True),
        sa.Column("photo_url", sa.String(length=512), nullable=True),
        sa.Column("lifestyle_tag_ids", postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column(
            "preferred_locality_ids", postgresql.ARRAY(sa.Integer()), nullable=True
        ),
        sa.Column("budget_min", sa.Integer(), nullable=True),
        sa.Column("budget_max", sa.Integer(), nullable=True),
        sa.Column("bhk_prefs", postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column("room_type_pref", sa.Integer(), nullable=True),
        sa.Column("furnishing_prefs", postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column("move_in_pref", sa.Integer(), nullable=True),
        sa.Column("move_in_date", sa.Date(), nullable=True),
        sa.Column("gender_pref", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)

    # ── Listings ───────────────────────────────────────────────────────────
    op.create_table(
        "listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "owner_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "locality_id",
            sa.Integer(),
            sa.ForeignKey("localities.id"),
            nullable=False,
        ),
        sa.Column("monthly_rent", sa.Integer(), nullable=False),
        sa.Column("bhk", sa.Integer(), nullable=False),
        sa.Column("furnishing", sa.Integer(), nullable=False),
        sa.Column("flatmates_needed", sa.Integer(), nullable=False),
        sa.Column("gender_pref", sa.Integer(), nullable=False),
        sa.Column("amenities", postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column("move_in", sa.Integer(), nullable=False),
        sa.Column("photos", postgresql.ARRAY(sa.String(length=512)), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_listings_owner_user_id", "listings", ["owner_user_id"])
    op.create_index("ix_listings_locality_id", "listings", ["locality_id"])

    # ── Teams ──────────────────────────────────────────────────────────────
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "owner_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_teams_owner_user_id", "teams", ["owner_user_id"])

    op.create_table(
        "team_members",
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    # ── Connection requests ────────────────────────────────────────────────
    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "from_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("target_kind", sa.Integer(), nullable=False),
        sa.Column(
            "target_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "target_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(target_kind = 1 AND target_user_id IS NOT NULL AND target_team_id IS NULL)"
            " OR (target_kind = 2 AND target_team_id IS NOT NULL AND target_user_id IS NULL)",
            name="ck_requests_target_consistency",
        ),
    )
    op.create_index("ix_requests_from_user_id", "requests", ["from_user_id"])
    op.create_index("ix_requests_target_user_id", "requests", ["target_user_id"])
    op.create_index("ix_requests_target_team_id", "requests", ["target_team_id"])
    op.create_index(
        "ux_requests_open_user_target",
        "requests",
        ["from_user_id", "target_user_id"],
        unique=True,
        postgresql_where=sa.text("target_kind = 1 AND status = 1"),
    )
    op.create_index(
        "ux_requests_open_team_target",
        "requests",
        ["from_user_id", "target_team_id"],
        unique=True,
        postgresql_where=sa.text("target_kind = 2 AND status = 1"),
    )

    op.create_table(
        "request_decisions",
        sa.Column(
            "request_id",
            sa.Integer(),
            sa.ForeignKey("requests.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("decision", sa.Integer(), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_request_decisions_user_id", "request_decisions", ["user_id"])

    # ── Rooms ──────────────────────────────────────────────────────────────
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "request_id",
            sa.Integer(),
            sa.ForeignKey("requests.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "flatmate_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_rooms_flatmate_team_id", "rooms", ["flatmate_team_id"])

    op.create_table(
        "room_participants",
        sa.Column(
            "room_id",
            sa.Integer(),
            sa.ForeignKey("rooms.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_room_participants_user_id", "room_participants", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_room_participants_user_id", table_name="room_participants")
    op.drop_table("room_participants")
    op.drop_index("ix_rooms_flatmate_team_id", table_name="rooms")
    op.drop_table("rooms")

    op.drop_index("ix_request_decisions_user_id", table_name="request_decisions")
    op.drop_table("request_decisions")

    op.drop_index("ux_requests_open_team_target", table_name="requests")
    op.drop_index("ux_requests_open_user_target", table_name="requests")
    op.drop_index("ix_requests_target_team_id", table_name="requests")
    op.drop_index("ix_requests_target_user_id", table_name="requests")
    op.drop_index("ix_requests_from_user_id", table_name="requests")
    op.drop_table("requests")

    op.drop_table("team_members")
    op.drop_index("ix_teams_owner_user_id", table_name="teams")
    op.drop_table("teams")

    op.drop_index("ix_listings_locality_id", table_name="listings")
    op.drop_index("ix_listings_owner_user_id", table_name="listings")
    op.drop_table("listings")

    op.drop_index("ix_users_phone", table_name="users")
    op.drop_table("users")
    op.drop_table("localities")
