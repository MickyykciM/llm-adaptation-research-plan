"""IPIP-style scoring utilities; not a claim of intrinsic model personality."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def score_trait(
    responses: Mapping[str, int],
    positive_item_ids: Sequence[str],
    reverse_item_ids: Sequence[str],
    scale_min: int = 1,
    scale_max: int = 5,
) -> int:
    required = set(positive_item_ids) | set(reverse_item_ids)
    missing = required - set(responses)
    if missing:
        raise ValueError(f"missing IPIP items: {sorted(missing)}")
    if any(not scale_min <= responses[item] <= scale_max for item in required):
        raise ValueError("IPIP responses outside scale")
    positive = sum(responses[item] for item in positive_item_ids)
    reverse = sum(scale_min + scale_max - responses[item] for item in reverse_item_ids)
    return positive + reverse


def trait_shift(pre_score: int, post_score: int) -> int:
    """Perceived context-conditioned change: post-context minus pre-context."""

    return post_score - pre_score
