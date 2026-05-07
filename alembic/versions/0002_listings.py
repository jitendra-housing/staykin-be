"""listings table; bhk, furnishing, move_in, gender_pref are integer ids.

Only the `amenity` Postgres ENUM type is created here (kept as ENUM until the
amenities vocabulary is finalized — at which point it converts to id-based too).
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_listings"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


AMENITY = ("PARKING", "AC", "KITCHEN", "WASHING_MACHINE", "LIFT", "BALCONY", "POOL")


def upgrade() -> None:
    bind = op.get_bind()
    amenity = postgresql.ENUM(*AMENITY, name="amenity")
    amenity.create(bind, checkfirst=True)

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
        sa.Column(
            "amenities",
            postgresql.ARRAY(postgresql.ENUM(*AMENITY, name="amenity", create_type=False)),
            nullable=True,
        ),
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


def downgrade() -> None:
    op.drop_index("ix_listings_locality_id", table_name="listings")
    op.drop_index("ix_listings_owner_user_id", table_name="listings")
    op.drop_table("listings")
    op.execute("DROP TYPE IF EXISTS amenity")
