"""Stable grouped splits with leakage checks."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Iterable


def stable_group_split(
    group_ids: Iterable[str],
    train_fraction: float = 0.60,
    validation_fraction: float = 0.20,
    salt: str = "adaptlab-v1",
) -> dict[str, str]:
    """Assign exact-size deterministic splits by salted hash rank."""

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be in (0, 1)")
    if not 0 <= validation_fraction < 1 - train_fraction:
        raise ValueError("validation_fraction leaves no test mass")

    unique_ids = sorted(set(group_ids))
    ranked = sorted(
        unique_ids,
        key=lambda group_id: hashlib.sha256(f"{salt}:{group_id}".encode()).digest(),
    )
    train_n = round(len(ranked) * train_fraction)
    validation_n = round(len(ranked) * validation_fraction)
    assignments: dict[str, str] = {}
    for index, group_id in enumerate(ranked):
        if index < train_n:
            split = "train"
        elif index < train_n + validation_n:
            split = "validation"
        else:
            split = "test"
        assignments[group_id] = split
    return assignments


def assert_group_disjoint(
    rows: Iterable[dict[str, object]], group_fields: tuple[str, ...]
) -> None:
    membership: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        split = str(row["split"])
        for field in group_fields:
            membership[(field, str(row[field]))].add(split)
    leaked = {key: values for key, values in membership.items() if len(values) > 1}
    if leaked:
        preview = list(leaked.items())[:5]
        raise ValueError(f"group leakage detected: {preview}")
