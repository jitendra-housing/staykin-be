"""Lifestyle tag affinity matrix used by vibe-compatibility scoring.

For every unordered pair of tags we store a score in [-1.0, +1.0]:
    +1.0  perfect synergy
     0.0  neutral / unrelated
    -1.0  total clash

The matrix is symmetric (A[i][j] == A[j][i]) and the diagonal is +1.0.
Below we only enumerate pairs that meaningfully synergise or clash; every
other pair is treated as 0.0 (neutral).

To tune scores: edit `_AFFINITY_PAIRS`. Validation runs at import.
"""

from app.db.seeds.lifestyle_tags import KEY_BY_ID, VALID_LIFESTYLE_TAG_IDS

# (tag_a_key, tag_b_key, score). Order within the pair does not matter;
# each pair must appear exactly once.
_AFFINITY_PAIRS: list[tuple[str, str, float]] = [
    # ── Sleep schedule ──
    ("LATE_NIGHTS", "EARLY_BIRDS", -0.85),

    # ── Noise / disruption vs. quiet & focus ──
    ("PARTY_OK", "QUIET_VIBES", -0.90),
    ("PARTY_OK", "WFH_GRIND", -0.70),
    ("PARTY_OK", "BOOKWORM", -0.55),
    ("PARTY_OK", "EARLY_BIRDS", -0.65),
    ("PARTY_OK", "NON_ALCOHOLIC", -0.30),
    ("PARTY_OK", "SMOKE_FREE", -0.20),
    ("PARTY_OK", "CLEAN_FREAK", -0.40),
    ("HOSTS_OFTEN", "QUIET_VIBES", -0.70),
    ("HOSTS_OFTEN", "WFH_GRIND", -0.45),
    ("HOSTS_OFTEN", "BOOKWORM", -0.35),
    ("HOSTS_OFTEN", "CLEAN_FREAK", -0.25),
    ("MUSIC_HEADS", "QUIET_VIBES", -0.45),
    ("MUSIC_HEADS", "WFH_GRIND", -0.30),
    ("MUSIC_HEADS", "BOOKWORM", -0.30),
    ("LATE_NIGHTS", "QUIET_VIBES", -0.40),
    ("LATE_NIGHTS", "WFH_GRIND", -0.35),
    ("GAMERS", "QUIET_VIBES", -0.30),
    ("GAMERS", "EARLY_BIRDS", -0.35),

    # ── Cleanliness friction ──
    ("CLEAN_FREAK", "PET_FRIENDLY", -0.30),
    ("CLEAN_FREAK", "LATE_NIGHTS", -0.15),

    # ── Diet alignment friction ──
    ("VEGAN", "FOODIES", -0.10),

    # ── Wellness cluster (synergy) ──
    ("YOGA_CHAI", "CHILL_VIBES", 0.80),
    ("YOGA_CHAI", "QUIET_VIBES", 0.70),
    ("YOGA_CHAI", "EARLY_BIRDS", 0.60),
    ("YOGA_CHAI", "VEGAN", 0.55),
    ("YOGA_CHAI", "NON_ALCOHOLIC", 0.55),
    ("YOGA_CHAI", "SMOKE_FREE", 0.45),
    ("YOGA_CHAI", "FITNESS_FREAK", 0.50),
    ("YOGA_CHAI", "PLANT_PARENTS", 0.50),
    ("VEGAN", "NON_ALCOHOLIC", 0.45),
    ("VEGAN", "SMOKE_FREE", 0.30),
    ("VEGAN", "FITNESS_FREAK", 0.35),
    ("NON_ALCOHOLIC", "SMOKE_FREE", 0.40),
    ("NON_ALCOHOLIC", "FITNESS_FREAK", 0.40),
    ("NON_ALCOHOLIC", "EARLY_BIRDS", 0.35),
    ("SMOKE_FREE", "FITNESS_FREAK", 0.40),
    ("SMOKE_FREE", "CLEAN_FREAK", 0.35),

    # ── Active / outdoors cluster ──
    ("FITNESS_FREAK", "SPORTY", 0.85),
    ("FITNESS_FREAK", "OUTDOORSY", 0.70),
    ("FITNESS_FREAK", "EARLY_BIRDS", 0.60),
    ("SPORTY", "OUTDOORSY", 0.70),
    ("SPORTY", "EARLY_BIRDS", 0.40),
    ("OUTDOORSY", "EARLY_BIRDS", 0.45),
    ("OUTDOORSY", "WANDERER", 0.65),
    ("OUTDOORSY", "PET_FRIENDLY", 0.40),

    # ── Quiet / focus cluster (synergy) ──
    ("BOOKWORM", "QUIET_VIBES", 0.80),
    ("BOOKWORM", "WFH_GRIND", 0.50),
    ("BOOKWORM", "CHILL_VIBES", 0.55),
    ("BOOKWORM", "PLANT_PARENTS", 0.40),
    ("BOOKWORM", "EARLY_BIRDS", 0.35),
    ("WFH_GRIND", "QUIET_VIBES", 0.75),
    ("WFH_GRIND", "CLEAN_FREAK", 0.40),
    ("WFH_GRIND", "PLANT_PARENTS", 0.40),
    ("QUIET_VIBES", "CHILL_VIBES", 0.55),
    ("QUIET_VIBES", "PLANT_PARENTS", 0.40),

    # ── Social / hosting cluster (synergy) ──
    ("HOSTS_OFTEN", "PARTY_OK", 0.70),
    ("HOSTS_OFTEN", "FOODIES", 0.65),
    ("HOSTS_OFTEN", "MUSIC_HEADS", 0.45),
    ("HOSTS_OFTEN", "MOVIE_NIGHTS", 0.45),
    ("HOSTS_OFTEN", "LATE_NIGHTS", 0.45),
    ("HOSTS_OFTEN", "CREATIVE", 0.30),
    ("PARTY_OK", "MUSIC_HEADS", 0.55),
    ("PARTY_OK", "LATE_NIGHTS", 0.65),
    ("PARTY_OK", "FOODIES", 0.35),

    # ── Late-night cluster ──
    ("LATE_NIGHTS", "MUSIC_HEADS", 0.40),
    ("LATE_NIGHTS", "GAMERS", 0.60),
    ("LATE_NIGHTS", "MOVIE_NIGHTS", 0.50),
    ("LATE_NIGHTS", "CREATIVE", 0.30),

    # ── Foodies cluster ──
    ("FOODIES", "CREATIVE", 0.30),
    ("FOODIES", "CHILL_VIBES", 0.30),
    ("FOODIES", "WANDERER", 0.40),
    ("FOODIES", "MOVIE_NIGHTS", 0.35),

    # ── Chill cluster ──
    ("CHILL_VIBES", "MOVIE_NIGHTS", 0.50),
    ("CHILL_VIBES", "PLANT_PARENTS", 0.40),
    ("CHILL_VIBES", "PET_FRIENDLY", 0.35),
    ("CHILL_VIBES", "CLEAN_FREAK", 0.20),

    # ── Creative cluster ──
    ("CREATIVE", "MUSIC_HEADS", 0.55),
    ("CREATIVE", "BOOKWORM", 0.40),
    ("CREATIVE", "WANDERER", 0.40),
    ("CREATIVE", "MOVIE_NIGHTS", 0.30),

    # ── Pets ──
    ("PET_FRIENDLY", "PLANT_PARENTS", 0.30),
    ("PET_FRIENDLY", "HOSTS_OFTEN", 0.20),

    # ── Indoor entertainment ──
    ("GAMERS", "MOVIE_NIGHTS", 0.45),
    ("GAMERS", "CREATIVE", 0.30),
]


def _build_matrix() -> list[list[float]]:
    """Materialise the sparse pair list into a dense lookup table.

    Index is the tag id (1..24); slot 0 is unused. Diagonal is +1.0,
    everything else defaults to 0.0 unless explicitly set in
    _AFFINITY_PAIRS. Validates symmetry, key validity, and uniqueness.
    """
    id_by_key = {key: tag_id for tag_id, key in KEY_BY_ID.items()}
    n = max(VALID_LIFESTYLE_TAG_IDS) + 1
    m: list[list[float]] = [[0.0] * n for _ in range(n)]
    for tag_id in VALID_LIFESTYLE_TAG_IDS:
        m[tag_id][tag_id] = 1.0

    seen: set[frozenset[str]] = set()
    for a_key, b_key, score in _AFFINITY_PAIRS:
        if a_key not in id_by_key:
            raise ValueError(f"unknown lifestyle tag key: {a_key!r}")
        if b_key not in id_by_key:
            raise ValueError(f"unknown lifestyle tag key: {b_key!r}")
        if a_key == b_key:
            raise ValueError(f"diagonal pair listed explicitly: {a_key!r}")
        if not -1.0 <= score <= 1.0:
            raise ValueError(f"score out of range for ({a_key},{b_key}): {score}")
        pair_key = frozenset((a_key, b_key))
        if pair_key in seen:
            raise ValueError(f"duplicate pair: ({a_key}, {b_key})")
        seen.add(pair_key)
        i, j = id_by_key[a_key], id_by_key[b_key]
        m[i][j] = score
        m[j][i] = score
    return m


AFFINITY: list[list[float]] = _build_matrix()


def affinity(tag_id_a: int, tag_id_b: int) -> float:
    """Look up the affinity score for two tag ids. Returns 0.0 if either
    id is outside the valid range (defensive — schema validation usually
    catches this earlier)."""
    if tag_id_a not in VALID_LIFESTYLE_TAG_IDS:
        return 0.0
    if tag_id_b not in VALID_LIFESTYLE_TAG_IDS:
        return 0.0
    return AFFINITY[tag_id_a][tag_id_b]
