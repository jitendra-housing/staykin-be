"""BHK options. DB stores integer ids."""

# (id, value, label)
BHKS: list[tuple[int, str, str]] = [
    (1, "ONE_BHK", "1BHK"),
    (2, "TWO_BHK", "2BHK"),
    (3, "THREE_BHK", "3BHK"),
    (4, "STUDIO", "Studio"),
]

VALID_BHK_IDS: frozenset[int] = frozenset(b[0] for b in BHKS)
