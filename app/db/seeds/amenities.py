"""Amenity options. DB stores integer ids."""

# (id, value, label)
AMENITIES: list[tuple[int, str, str]] = [
    (1, "WIFI", "WiFi"),
    (2, "AC", "AC"),
    (3, "GEYSER", "Geyser"),
    (4, "WASHER", "Washing machine"),
    (5, "CCTV", "CCTV"),
    (6, "PARKING", "Parking"),
    (7, "LIFT", "Lift"),
    (8, "GYM", "Gym"),
    (9, "FURNISHED", "Furnished"),
    (10, "ATTACHED_BATH", "Attached bath"),
    (11, "POOL", "Pool"),
    (12, "WFH_READY", "WFH ready"),
    (13, "BALCONY", "Balcony"),
]

VALID_AMENITY_IDS: frozenset[int] = frozenset(a[0] for a in AMENITIES)
