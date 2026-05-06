"""Static lifestyle-tag vocabulary. Edit here to add/remove tags.
DB stores only the integer ids on users.lifestyle_tag_ids.
"""

# (id, key, label)
LIFESTYLE_TAGS: list[tuple[int, str, str]] = [
    (1, "PLANT_PARENTS", "Plant parents"),
    (2, "WFH_GRIND", "WFH grind"),
    (3, "MUSIC_HEADS", "Music heads"),
    (4, "BOOKWORM", "Bookworm"),
    (5, "YOGA_CHAI", "Yoga + chai"),
    (6, "FOODIES", "Foodies"),
    (7, "LATE_NIGHTS", "Late nights"),
    (8, "EARLY_BIRDS", "Early birds"),
    (9, "PET_FRIENDLY", "Pet friendly"),
    (10, "SMOKE_FREE", "Smoke free"),
    (11, "QUIET_VIBES", "Quiet vibes"),
    (12, "PARTY_OK", "Party ok"),
    (13, "CREATIVE", "Creative"),
    (14, "OUTDOORSY", "Outdoorsy"),
    (15, "HOSTS_OFTEN", "Hosts often"),
    (16, "FITNESS_FREAK", "Fitness freak"),
    (17, "VEGAN", "Vegan"),
    (18, "NON_ALCOHOLIC", "Non-alcoholic"),
    (19, "WANDERER", "Wanderer"),
    (20, "CLEAN_FREAK", "Clean freak"),
    (21, "CHILL_VIBES", "Chill vibes"),
    (22, "GAMERS", "Gamers"),
    (23, "MOVIE_NIGHTS", "Movie nights"),
    (24, "SPORTY", "Sporty"),
]

VALID_LIFESTYLE_TAG_IDS: frozenset[int] = frozenset(t[0] for t in LIFESTYLE_TAGS)
LABEL_BY_ID: dict[int, str] = {t[0]: t[2] for t in LIFESTYLE_TAGS}
KEY_BY_ID: dict[int, str] = {t[0]: t[1] for t in LIFESTYLE_TAGS}

MIN_TAGS = 5
MAX_TAGS = 10
