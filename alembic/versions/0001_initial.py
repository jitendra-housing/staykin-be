"""initial schema: users, localities + seed Gurgaon localities"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.db.seeds.localities import LOCALITIES

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


GENDER = ("MALE", "FEMALE", "OTHER")
BHK = ("STUDIO", "ONE_BHK", "TWO_BHK", "THREE_BHK", "FOUR_BHK", "FIVE_BHK")
ROOM_TYPE = ("SINGLE", "SHARING", "BOTH")
FURNISHING = ("FULL", "SEMI", "UNFURNISHED")
MOVE_IN = ("ASAP", "WITHIN_1_MONTH", "ONE_TO_THREE_MONTHS")
SLEEP = ("EARLY_BIRD", "NIGHT_OWL", "FLEXIBLE")
CLEAN = ("VERY_TIDY", "AVERAGE", "RELAXED")
YNS = ("YES", "NO", "SOMETIMES")
FOOD = ("VEG", "NON_VEG", "EGGITARIAN")
FREQ = ("OFTEN", "SOMETIMES", "RARELY")


def upgrade() -> None:
    # Create enum types first (so ARRAY columns can reference them).
    gender = postgresql.ENUM(*GENDER, name="gender")
    gender_pref = postgresql.ENUM(*GENDER, name="gender_pref")
    bhk = postgresql.ENUM(*BHK, name="bhk")
    room_type = postgresql.ENUM(*ROOM_TYPE, name="room_type")
    furnishing = postgresql.ENUM(*FURNISHING, name="furnishing")
    move_in = postgresql.ENUM(*MOVE_IN, name="move_in")
    sleep_schedule = postgresql.ENUM(*SLEEP, name="sleep_schedule")
    cleanliness = postgresql.ENUM(*CLEAN, name="cleanliness")
    smoking = postgresql.ENUM(*YNS, name="smoking_pref")
    drinking = postgresql.ENUM(*YNS, name="drinking_pref")
    food_pref = postgresql.ENUM(*FOOD, name="food_pref")
    pets = postgresql.ENUM(*YNS, name="pets_pref")
    guests = postgresql.ENUM(*FREQ, name="guests_frequency")
    wfh = postgresql.ENUM(*FREQ, name="wfh_frequency")
    noise = postgresql.ENUM(*FREQ, name="noise_tolerance")

    bind = op.get_bind()
    for enum in (
        gender,
        gender_pref,
        bhk,
        room_type,
        furnishing,
        move_in,
        sleep_schedule,
        cleanliness,
        smoking,
        drinking,
        food_pref,
        pets,
        guests,
        wfh,
        noise,
    ):
        enum.create(bind, checkfirst=True)

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

    # Seed localities (using the IDs we want).
    op.bulk_insert(
        sa.table(
            "localities",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [{"id": _id, "name": name} for _id, name in LOCALITIES],
    )
    # Reset sequence past the seeded IDs.
    op.execute(
        "SELECT setval(pg_get_serial_sequence('localities', 'id'), "
        "(SELECT MAX(id) FROM localities))"
    )

    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("phone", sa.String(length=20), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "gender",
            postgresql.ENUM(*GENDER, name="gender", create_type=False),
            nullable=True,
        ),
        sa.Column("occupation", sa.String(length=120), nullable=True),
        sa.Column("photo_url", sa.String(length=512), nullable=True),
        sa.Column(
            "sleep_schedule",
            postgresql.ENUM(*SLEEP, name="sleep_schedule", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "cleanliness",
            postgresql.ENUM(*CLEAN, name="cleanliness", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "smoking",
            postgresql.ENUM(*YNS, name="smoking_pref", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "drinking",
            postgresql.ENUM(*YNS, name="drinking_pref", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "food_pref",
            postgresql.ENUM(*FOOD, name="food_pref", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "pets",
            postgresql.ENUM(*YNS, name="pets_pref", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "guests_frequency",
            postgresql.ENUM(*FREQ, name="guests_frequency", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "work_from_home",
            postgresql.ENUM(*FREQ, name="wfh_frequency", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "noise_tolerance",
            postgresql.ENUM(*FREQ, name="noise_tolerance", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "languages",
            postgresql.ARRAY(sa.String(length=40)),
            nullable=True,
        ),
        sa.Column(
            "preferred_locality_ids",
            postgresql.ARRAY(sa.Integer()),
            nullable=True,
        ),
        sa.Column("budget_min", sa.Integer(), nullable=True),
        sa.Column("budget_max", sa.Integer(), nullable=True),
        sa.Column(
            "bhk_prefs",
            postgresql.ARRAY(postgresql.ENUM(*BHK, name="bhk", create_type=False)),
            nullable=True,
        ),
        sa.Column(
            "room_type_pref",
            postgresql.ENUM(*ROOM_TYPE, name="room_type", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "furnishing_prefs",
            postgresql.ARRAY(
                postgresql.ENUM(*FURNISHING, name="furnishing", create_type=False)
            ),
            nullable=True,
        ),
        sa.Column(
            "move_in_pref",
            postgresql.ENUM(*MOVE_IN, name="move_in", create_type=False),
            nullable=True,
        ),
        sa.Column("move_in_date", sa.Date(), nullable=True),
        sa.Column(
            "gender_pref",
            postgresql.ENUM(*GENDER, name="gender_pref", create_type=False),
            nullable=True,
        ),
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

    for name in (
        "noise_tolerance",
        "wfh_frequency",
        "guests_frequency",
        "pets_pref",
        "food_pref",
        "drinking_pref",
        "smoking_pref",
        "cleanliness",
        "sleep_schedule",
        "move_in",
        "furnishing",
        "room_type",
        "bhk",
        "gender_pref",
        "gender",
    ):
        op.execute(f"DROP TYPE IF EXISTS {name}")
