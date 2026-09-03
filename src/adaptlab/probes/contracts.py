"""Contracts that make temporal leakage auditable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureDescriptor:
    name: str
    family: str
    source_turn: str
    capture_boundary: str
    uses_target_response: bool = False

    def validate(self) -> None:
        if self.uses_target_response:
            raise ValueError(f"{self.name} violates the pre-response forecast boundary")
        if self.capture_boundary not in {"after_previous_response", "after_next_user_message"}:
            raise ValueError("unknown capture boundary")


ALLOWED_FAMILIES = {
    "surface",
    "semantic",
    "prompt_logits",
    "residual_stream",
    "cross_turn_delta",
    "attention_summary",
    "head_output",
    "counterfactual_continuations",
    "difficulty_control",
}
