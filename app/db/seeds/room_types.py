"""Room types. DB stores integer ids."""

# (id, value, label)
ROOM_TYPES: list[tuple[int, str, str]] = [
    (1, "SINGLE_ROOM", "Single Room"),
    (2, "SHARING", "Sharing"),
    (3, "EITHER", "Either"),
]

VALID_ROOM_TYPE_IDS: frozenset[int] = frozenset(r[0] for r in ROOM_TYPES)
