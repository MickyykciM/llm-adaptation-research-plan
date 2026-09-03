"""Model-agnostic request and capture contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class CaptureSpec:
    residual_layers: tuple[int, ...] = ()
    record_prompt_logits: bool = True
    attention_summary: bool = False
    head_outputs: tuple[tuple[int, int], ...] = ()
    enforce_pre_target_capture: bool = True


@dataclass
class PreGenerationSnapshot:
    prompt_token_count: int
    prompt_logits: Any | None = None
    residuals: dict[int, Any] = field(default_factory=dict)
    attention_summaries: dict[str, Any] = field(default_factory=dict)
    head_outputs: dict[tuple[int, int], Any] = field(default_factory=dict)
    captured_before_target_generation: bool = True


@dataclass
class Generation:
    text: str
    token_ids: Sequence[int]
    seed: int
    latency_seconds: float


class ModelAdapter(Protocol):
    model_id: str
    model_revision: str

    def capture_before_generation(
        self, messages: Sequence[ChatMessage], spec: CaptureSpec
    ) -> PreGenerationSnapshot:
        ...

    def generate(
        self,
        messages: Sequence[ChatMessage],
        *,
        seed: int,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
    ) -> Generation:
        ...
