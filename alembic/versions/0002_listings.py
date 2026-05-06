"""listings table + listing_gender_pref + amenity enums"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_listings"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


LISTING_GENDER_PREF = ("GIRLS_ONLY", "BOYS_ONLY", "MIXED")
AMENITY = ("PARKING", "AC", "KITCHEN", "WASHING_MACHINE", "LIFT", "BALCONY", "POOL")
BHK = ("STUDIO", "ONE_BHK", "TWO_BHK", "THREE_BHK", "FOUR_BHK", "FIVE_BHK")
FURNISHING = ("FULL", "SEMI", "UNFURNISHED")
MOVE_IN = ("ASAP", "WITHIN_1_MONTH", "ONE_TO_THREE_MONTHS")


def upgrade() -> None:
    bind = op.get_bind()

    listing_gender_pref = postgresql.ENUM(*LISTING_GENDER_PREF, name="listing_gender_pref")
    amenity = postgresql.ENUM(*AMENITY, name="amenity")
    listing_gender_pref.create(bind, checkfirst=True)
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
        sa.Column(
            "bhk",
            postgresql.ENUM(*BHK, name="bhk", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "furnishing",
            postgresql.ENUM(*FURNISHING, name="furnishing", create_type=False),
            nullable=False,
        ),
        sa.Column("flatmates_needed", sa.Integer(), nullable=False),
        sa.Column(
            "gender_pref",
            postgresql.ENUM(
                *LISTING_GENDER_PREF, name="listing_gender_pref", create_type=False
            ),
            nullable=False,
        ),
        sa.Column(
            "amenities",
            postgresql.ARRAY(postgresql.ENUM(*AMENITY, name="amenity", create_type=False)),
            nullable=True,
        ),
        sa.Column(
            "move_in",
            postgresql.ENUM(*MOVE_IN, name="move_in", create_type=False),
            nullable=False,
        ),
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
    op.execute("DROP TYPE IF EXISTS listing_gender_pref")
