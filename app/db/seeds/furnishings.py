"""Furnishing options. DB stores integer ids."""

# (id, value, label)
FURNISHINGS: list[tuple[int, str, str]] = [
    (1, "FURNISHED", "Furnished"),
    (2, "SEMI", "Semi"),
    (3, "UNFURNISHED", "Unfurnished"),
]

VALID_FURNISHING_IDS: frozenset[int] = frozenset(f[0] for f in FURNISHINGS)
