"""Per-target decision statuses on a request. DB stores integer ids on request_decisions.decision."""

# (id, value, label)
DECISION_STATUSES: list[tuple[int, str, str]] = [
    (1, "PENDING", "Pending"),
    (2, "ACCEPTED", "Accepted"),
    (3, "REJECTED", "Rejected"),
]

VALID_DECISION_STATUS_IDS: frozenset[int] = frozenset(s[0] for s in DECISION_STATUSES)

DECISION_PENDING = 1
DECISION_ACCEPTED = 2
DECISION_REJECTED = 3
