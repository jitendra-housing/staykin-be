"""initial schema: users, localities + seed Gurgaon localities

All categorical fields (gender, bhk, room_type, furnishing, move_in, ...) are
stored as integer ids referencing the constants in app/db/seeds/. No Postgres
ENUM types are created here.
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
    # Localities
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

    # Users — all categorical fields are integer ids.
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("phone", sa.String(length=20), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.Integer(), nullable=True),
        sa.Column("occupation", sa.String(length=120), nullable=True),
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


def downgrade() -> None:
    op.drop_index("ix_users_phone", table_name="users")
    op.drop_table("users")
    op.drop_table("localities")
