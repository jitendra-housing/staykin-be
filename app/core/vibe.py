"""Vibe compatibility scoring between two users.

The score answers: "how well do these two people's lifestyle preferences
go together?" It is computed by looking up every cross-pair of their
lifestyle tags in the precomputed affinity matrix, averaging the
results, and mapping the [-1, +1] range to a friendly 0-100 percentage.

There is no AI call at runtime — all the semantic judgement lives in
the matrix at app/db/seeds/lifestyle_affinity.py.
"""

from collections.abc import Iterable

from app.db.seeds.lifestyle_affinity import AFFINITY


def vibe_score(tags_a: Iterable[int] | None, tags_b: Iterable[int] | None) -> int | None:
    """Return a 0-100 vibe compatibility score, or None if either user
    has not selected lifestyle preferences yet.

    Uses the cross-product of tag sets, averaged through the affinity
    matrix, then linearly mapped from [-1, +1] to [0, 100].
    """
    a = list(tags_a or ())
    b = list(tags_b or ())
    if not a or not b:
        return None

    total = 0.0
    for i in a:
        row = AFFINITY[i]
        for j in b:
            total += row[j]
    raw = total / (len(a) * len(b))
    return round(((raw + 1.0) / 2.0) * 100)
