"""Amenity options. DB stores integer ids."""

# (id, value, label)
AMENITIES: list[tuple[int, str, str]] = [
    (1, "PARKING", "Parking"),
    (2, "AIR_CONDITIONING", "AC"),
    (3, "KITCHEN", "Kitchen"),
    (4, "WASHING_MACHINE", "Washing m/c"),
    (5, "LIFT", "Lift"),
    (6, "BALCONY", "Balcony"),
    (7, "POOL", "Pool"),
]

VALID_AMENITY_IDS: frozenset[int] = frozenset(a[0] for a in AMENITIES)
