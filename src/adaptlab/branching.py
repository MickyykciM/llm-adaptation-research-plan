"""Count and materialize preregistered pilot-factor assignments."""

from __future__ import annotations

import itertools
import tomllib
from collections.abc import Iterator
from pathlib import Path
from typing import Any


COUNT_KEYS = {
    "core": (
        "questions",
        "initial_states",
        "evidence_profiles",
        "pressure_levels",
        "template_families",
        "samples",
        "styles",
    ),
    "causal": (
        "questions",
        "initial_states",
        "evidence_profiles",
        "pressure_levels",
        "template_families",
        "samples",
        "styles",
    ),
    "mitigation": ("contexts", "arms", "samples"),
}


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("rb") as handle:
        return tomllib.load(handle)


def section_count(section_name: str, section: dict[str, Any]) -> int:
    product = 1
    for key in COUNT_KEYS[section_name]:
        value = int(section[key])
        if value < 1:
            raise ValueError(f"{section_name}.{key} must be positive")
        product *= value
    return product


def generation_counts(config: dict[str, Any]) -> dict[str, int]:
    counts = {
        section: section_count(section, config[section]) for section in COUNT_KEYS
    }
    counts["total"] = sum(counts.values())
    return counts


def _factor_indices(section_name: str, section: dict[str, Any]) -> Iterator[dict[str, int | str]]:
    keys = COUNT_KEYS[section_name]
    ranges = [range(int(section[key])) for key in keys]
    for serial, values in enumerate(itertools.product(*ranges)):
        row: dict[str, int | str] = {
            "trial_id": f"{section_name}-{serial:06d}",
            "block": section_name,
        }
        row.update(dict(zip(keys, values, strict=True)))
        yield row


def iter_factor_rows(config: dict[str, Any]) -> Iterator[dict[str, int | str]]:
    """Yield design-cell indices, not prompts, labels, or model outputs."""

    for section_name in COUNT_KEYS:
        yield from _factor_indices(section_name, config[section_name])
