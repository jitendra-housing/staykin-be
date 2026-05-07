"""rooms.flatmate_team_id: link from a room to the team produced by Add Flatmate."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_room_flatmate_team"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "rooms",
        sa.Column("flatmate_team_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_rooms_flatmate_team_id",
        "rooms",
        "teams",
        ["flatmate_team_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_rooms_flatmate_team_id", "rooms", ["flatmate_team_id"])


def downgrade() -> None:
    op.drop_index("ix_rooms_flatmate_team_id", table_name="rooms")
    op.drop_constraint("fk_rooms_flatmate_team_id", "rooms", type_="foreignkey")
    op.drop_column("rooms", "flatmate_team_id")
