"""Typed records shared by generation, evaluation, and analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class EvidenceValidity(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    AMBIGUOUS = "ambiguous"
    NOT_APPLICABLE = "not_applicable"


class EvidenceRelevance(StrEnum):
    RELEVANT = "relevant"
    IRRELEVANT = "irrelevant"
    PARTIALLY_RELEVANT = "partially_relevant"


class EvidenceRelation(StrEnum):
    SUPPORTS_GOLD = "supports_gold"
    CONTRADICTS_GOLD = "contradicts_gold"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class RevisionOutcome(StrEnum):
    JUSTIFIED_PERSISTENCE = "justified_persistence"
    HARMFUL_DRIFT = "harmful_drift"
    BENEFICIAL_CORRECTION = "beneficial_correction"
    STUBBORNNESS = "stubbornness"
    JUSTIFIED_SUPPORT = "justified_support"
    UNSUPPORTED_LUCKY_CORRECTION = "unsupported_lucky_correction"
    WRONG_TO_DIFFERENT_WRONG = "wrong_to_different_wrong"
    JUSTIFIED_ABSTENTION = "justified_abstention"
    OVERCAUTIOUS_ABSTENTION = "overcautious_abstention"
    UNPARSEABLE = "unparseable"
    OTHER = "other"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    text: str
    validity: EvidenceValidity
    relevance: EvidenceRelevance
    diagnostic_strength: float
    source_reliability: float
    relation_to_gold: EvidenceRelation
    rhetorical_pressure: str
    repetition_count: int = 1
    independence_group: str = "primary"
    provenance: str = "synthetic"
    generator_version: str = "unversioned"

    def validate(self) -> None:
        for name, value in (
            ("diagnostic_strength", self.diagnostic_strength),
            ("source_reliability", self.source_reliability),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.repetition_count < 1:
            raise ValueError("repetition_count must be positive")
        if not self.evidence_id:
            raise ValueError("evidence_id must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


@dataclass
class TrialRecord:
    trial_id: str
    question_family_id: str
    stage: str
    challenge_template_family: str
    initial_answer: str
    initial_correct: bool
    previous_style: str
    evidence: EvidenceRecord
    final_answer: str | None = None
    final_correct: bool | None = None
    evidence_assessment_correct: bool | None = None
    abstained: bool = False
    generation_seed: int | None = None
    split: str | None = None
    prompt_sha256: str | None = None
    model_id: str | None = None
    model_revision: str | None = None
    feature_timestamp: str = "pre_target_generation"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate_pre_response_features(self) -> None:
        forbidden = {
            "target_hidden_states",
            "target_attention",
            "target_head_outputs",
            "target_logits_after_first_token",
        }
        leaked = forbidden.intersection(self.metadata)
        if leaked:
            raise ValueError(f"target-response leakage fields present: {sorted(leaked)}")
        if self.feature_timestamp != "pre_target_generation":
            raise ValueError("forecast features must be captured before target generation")

    def to_dict(self) -> dict[str, Any]:
        self.evidence.validate()
        self.validate_pre_response_features()
        return asdict(self)
