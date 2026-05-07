"""Request target kinds. DB stores integer ids on requests.target_kind."""

# (id, value, label)
REQUEST_TARGET_KINDS: list[tuple[int, str, str]] = [
    (1, "USER", "User"),
    (2, "TEAM", "Team"),
]

VALID_REQUEST_TARGET_KIND_IDS: frozenset[int] = frozenset(k[0] for k in REQUEST_TARGET_KINDS)

TARGET_KIND_USER = 1
TARGET_KIND_TEAM = 2
