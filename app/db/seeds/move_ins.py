"""Move-in options. DB stores integer ids."""

# (id, value, label)
MOVE_INS: list[tuple[int, str, str]] = [
    (1, "ASAP", "ASAP"),
    (2, "WITHIN_ONE_MONTH", "Within 1 month"),
    (3, "ONE_TO_THREE_MONTHS", "1–3 months"),
]

VALID_MOVE_IN_IDS: frozenset[int] = frozenset(m[0] for m in MOVE_INS)
