"""listings.room_type: which room type the listing offers (single / sharing / either)."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_listings_room_type"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "listings",
        sa.Column("room_type", sa.Integer(), nullable=False, server_default="3"),
    )
    op.alter_column("listings", "room_type", server_default=None)


def downgrade() -> None:
    op.drop_column("listings", "room_type")
