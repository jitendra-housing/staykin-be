"""Only enums whose values still live in the DB as Postgres ENUM types remain here.

All other categorical fields (gender, bhk, furnishing, move_in, room_type,
listing_gender_pref, lifestyle_tags, localities) are now id-based, with the
canonical lists defined in app/db/seeds/.
"""

import enum


class Amenity(str, enum.Enum):
    PARKING = "PARKING"
    AC = "AC"
    KITCHEN = "KITCHEN"
    WASHING_MACHINE = "WASHING_MACHINE"
    LIFT = "LIFT"
    BALCONY = "BALCONY"
    POOL = "POOL"
