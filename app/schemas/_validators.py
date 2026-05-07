"""Reusable Pydantic validators for id-based fields backed by code constants."""


def validate_id(v: int | None, valid: frozenset[int], field: str) -> int | None:
    if v is None:
        return v
    if v not in valid:
        raise ValueError(f"unknown {field} id: {v}")
    return v


def validate_id_list(
    v: list[int] | None,
    valid: frozenset[int],
    field: str,
    min_len: int | None = None,
    max_len: int | None = None,
) -> list[int] | None:
    if v is None or len(v) == 0:
        return v
    if len(v) != len(set(v)):
        raise ValueError(f"{field} ids must be unique")
    invalid = sorted(set(v) - valid)
    if invalid:
        raise ValueError(f"unknown {field} ids: {invalid}")
    if min_len is not None and len(v) < min_len:
        raise ValueError(f"{field} requires at least {min_len} items")
    if max_len is not None and len(v) > max_len:
        raise ValueError(f"{field} allows at most {max_len} items")
    return v
