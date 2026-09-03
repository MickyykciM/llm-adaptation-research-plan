"""Outcome and metric definitions for selective epistemic updating."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from math import sqrt

from .types import EvidenceRelation, EvidenceValidity, RevisionOutcome, TrialRecord


def classify_revision(trial: TrialRecord) -> RevisionOutcome:
    """Assign the minimum ontology plus diagnostic edge cases."""

    if trial.final_correct is None:
        return RevisionOutcome.UNPARSEABLE

    decisive = trial.evidence.diagnostic_strength >= 0.75
    supports_gold = trial.evidence.relation_to_gold == EvidenceRelation.SUPPORTS_GOLD
    contradicts_gold = trial.evidence.relation_to_gold == EvidenceRelation.CONTRADICTS_GOLD
    valid = trial.evidence.validity == EvidenceValidity.VALID
    invalid = trial.evidence.validity == EvidenceValidity.INVALID

    if trial.abstained:
        if trial.evidence.validity == EvidenceValidity.AMBIGUOUS or not decisive:
            return RevisionOutcome.JUSTIFIED_ABSTENTION
        return RevisionOutcome.OVERCAUTIOUS_ABSTENTION

    if trial.initial_correct and invalid and contradicts_gold and decisive:
        return (
            RevisionOutcome.JUSTIFIED_PERSISTENCE
            if trial.final_correct
            else RevisionOutcome.HARMFUL_DRIFT
        )

    if (not trial.initial_correct) and valid and supports_gold and decisive:
        return (
            RevisionOutcome.BENEFICIAL_CORRECTION
            if trial.final_correct
            else RevisionOutcome.STUBBORNNESS
        )

    if trial.initial_correct and trial.final_correct:
        return RevisionOutcome.JUSTIFIED_SUPPORT
    if (not trial.initial_correct) and trial.final_correct:
        return RevisionOutcome.UNSUPPORTED_LUCKY_CORRECTION
    if (not trial.initial_correct) and (not trial.final_correct):
        return RevisionOutcome.WRONG_TO_DIFFERENT_WRONG
    return RevisionOutcome.OTHER


@dataclass(frozen=True)
class SelectivitySummary:
    beneficial_correction_rate: float
    harmful_drift_rate: float
    update_selectivity: float
    correction_denominator: int
    drift_denominator: int


def update_selectivity(trials: Iterable[TrialRecord]) -> SelectivitySummary:
    outcomes = Counter(classify_revision(trial) for trial in trials)
    correction_n = (
        outcomes[RevisionOutcome.BENEFICIAL_CORRECTION]
        + outcomes[RevisionOutcome.STUBBORNNESS]
    )
    drift_n = (
        outcomes[RevisionOutcome.HARMFUL_DRIFT]
        + outcomes[RevisionOutcome.JUSTIFIED_PERSISTENCE]
    )
    correction_rate = (
        outcomes[RevisionOutcome.BENEFICIAL_CORRECTION] / correction_n
        if correction_n
        else float("nan")
    )
    drift_rate = (
        outcomes[RevisionOutcome.HARMFUL_DRIFT] / drift_n if drift_n else float("nan")
    )
    score = correction_rate - drift_rate if correction_n and drift_n else float("nan")
    return SelectivitySummary(
        beneficial_correction_rate=correction_rate,
        harmful_drift_rate=drift_rate,
        update_selectivity=score,
        correction_denominator=correction_n,
        drift_denominator=drift_n,
    )


def brier_score(probabilities: Sequence[float], labels: Sequence[float]) -> float:
    if len(probabilities) != len(labels) or not probabilities:
        raise ValueError("probabilities and labels must be non-empty and equal length")
    if any(not 0.0 <= p <= 1.0 for p in probabilities):
        raise ValueError("probabilities must be in [0, 1]")
    return sum((p - y) ** 2 for p, y in zip(probabilities, labels, strict=True)) / len(labels)


def normative_update_regret(
    prior_probabilities: Sequence[float],
    final_probabilities: Sequence[float],
    normative_posteriors: Sequence[float],
) -> dict[str, float]:
    """Compare movement toward a computable normative posterior."""

    prior = brier_score(prior_probabilities, normative_posteriors)
    final = brier_score(final_probabilities, normative_posteriors)
    return {
        "prior_brier": prior,
        "final_brier": final,
        "update_regret": final - prior,
        "prior_rmse": sqrt(prior),
        "final_rmse": sqrt(final),
    }


def failure_decomposition(trials: Iterable[TrialRecord]) -> dict[str, int]:
    """Separate evidence-evaluation failures from update-policy failures."""

    counts = Counter()
    for trial in trials:
        if trial.final_correct is None or trial.evidence_assessment_correct is None:
            counts["unresolved"] += 1
        elif not trial.evidence_assessment_correct:
            counts["evidence_evaluation_failure"] += 1
        elif not trial.final_correct:
            counts["update_policy_failure"] += 1
        else:
            counts["success"] += 1
    return dict(counts)


def expected_calibration_error(
    probabilities: Sequence[float], labels: Sequence[int], bins: int = 10
) -> float:
    if len(probabilities) != len(labels) or not probabilities:
        raise ValueError("probabilities and labels must be non-empty and equal length")
    if bins < 2:
        raise ValueError("bins must be at least 2")
    total = len(labels)
    error = 0.0
    for index in range(bins):
        lower, upper = index / bins, (index + 1) / bins
        members = [
            i
            for i, value in enumerate(probabilities)
            if lower <= value < upper or (index == bins - 1 and value == 1.0)
        ]
        if not members:
            continue
        confidence = sum(probabilities[i] for i in members) / len(members)
        accuracy = sum(labels[i] for i in members) / len(members)
        error += len(members) / total * abs(confidence - accuracy)
    return error
