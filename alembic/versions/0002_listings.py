"""listings table; all categorical fields are integer ids (no Postgres ENUM types)."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_listings"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.drop_index("ix_listings_locality_id", table_name="listings")
    op.drop_index("ix_listings_owner_user_id", table_name="listings")
    op.drop_table("listings")
