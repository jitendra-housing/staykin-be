"""Request lifecycle statuses. DB stores integer ids on requests.status."""

# (id, value, label)
REQUEST_STATUSES: list[tuple[int, str, str]] = [
    (1, "IN_PROGRESS", "In progress"),
    (2, "ACCEPTED", "Accepted"),
    (3, "REJECTED", "Rejected"),
]

VALID_REQUEST_STATUS_IDS: frozenset[int] = frozenset(s[0] for s in REQUEST_STATUSES)

REQUEST_STATUS_IN_PROGRESS = 1
REQUEST_STATUS_ACCEPTED = 2
REQUEST_STATUS_REJECTED = 3
