"""Listing-level gender preference options. DB stores integer ids."""

# (id, value, label)
LISTING_GENDER_PREFS: list[tuple[int, str, str]] = [
    (1, "GIRLS_ONLY", "Girls Only"),
    (2, "BOYS_ONLY", "Boys Only"),
    (3, "MIXED", "Mixed"),
]

VALID_LISTING_GENDER_PREF_IDS: frozenset[int] = frozenset(p[0] for p in LISTING_GENDER_PREFS)
