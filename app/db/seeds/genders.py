"""Static gender vocabulary. DB stores integer ids on user.gender / user.gender_pref."""

# (id, value, label)
GENDERS: list[tuple[int, str, str]] = [
    (1, "MALE", "Male"),
    (2, "FEMALE", "Female"),
    (3, "OTHER", "Other"),
]

VALID_GENDER_IDS: frozenset[int] = frozenset(g[0] for g in GENDERS)

GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_OTHER = 3
