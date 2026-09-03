"""Selective mitigation gate and cost-aware evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    trigger: bool
    risk: float
    threshold: float
    action: str


def select_action(risk: float, threshold: float, action: str = "verify_evidence") -> GateDecision:
    if not 0.0 <= risk <= 1.0:
        raise ValueError("risk must be in [0, 1]")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    return GateDecision(trigger=risk >= threshold, risk=risk, threshold=threshold, action=action)


def mitigation_utility(
    errors_prevented: int,
    false_alarms: int,
    added_seconds: float,
    added_tokens: int,
    *,
    false_alarm_cost: float = 0.25,
    second_cost: float = 0.01,
    token_cost: float = 0.00001,
) -> float:
    return (
        float(errors_prevented)
        - false_alarm_cost * false_alarms
        - second_cost * added_seconds
        - token_cost * added_tokens
    )
