"""Deterministic answer normalization for mechanically labeled tasks."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation


_SPACE = re.compile(r"\s+")
_PUNCT = re.compile(r"^[\s\"'\x60.,:;!?()\[\]{}]+|[\s\"'\x60.,:;!?()\[\]{}]+$")


def normalize_answer(text: str) -> str:
    value = _SPACE.sub(" ", text.strip().casefold())
    return _PUNCT.sub("", value)


def exact_match(prediction: str, gold: str) -> bool:
    return normalize_answer(prediction) == normalize_answer(gold)


def numeric_match(prediction: str, gold: str, tolerance: Decimal = Decimal("0")) -> bool:
    try:
        predicted = Decimal(normalize_answer(prediction).replace(",", ""))
        expected = Decimal(normalize_answer(gold).replace(",", ""))
    except InvalidOperation:
        return False
    return abs(predicted - expected) <= tolerance
