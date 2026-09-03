"""Offline checks for counts, schemas, templates, and documentation safeguards."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.branching import generation_counts, load_config


def main() -> None:
    config = load_config(ROOT / "configs" / "pilot.toml")
    counts = generation_counts(config)
    expected = {"core": 23040, "causal": 1536, "mitigation": 1024, "total": 25600}
    if counts != expected:
        raise AssertionError(f"generation-count mismatch: {counts}")

    profiles = json.loads(
        (ROOT / "data" / "templates" / "evidence_profiles.json").read_text(encoding="utf-8")
    )
    if len(profiles) != 8 or len({item["profile_id"] for item in profiles}) != 8:
        raise AssertionError("expected eight unique evidence profiles")
    required = {
        "validity",
        "relevance",
        "diagnostic_strength",
        "source_reliability",
        "relation_to_gold",
        "rhetorical_pressure",
        "repetition_count",
        "independence_group",
    }
    for profile in profiles:
        missing = required - set(profile)
        if missing:
            raise AssertionError(f"{profile['profile_id']} missing {sorted(missing)}")

    schema_paths = list((ROOT / "schemas").glob("*.json"))
    if len(schema_paths) < 4:
        raise AssertionError("expected at least four JSON schemas")
    for schema_path in schema_paths:
        json.loads(schema_path.read_text(encoding="utf-8"))

    plan = (ROOT / "docs" / "RESEARCH_PLAN.md").read_text(encoding="utf-8")
    required_phrases = [
        "no empirical results",
        "target-response activations",
        "PreferenceDrift-Bench",
        "2026-09-02",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in plan]
    if missing_phrases:
        raise AssertionError(f"research plan missing safeguards: {missing_phrases}")
    print(json.dumps({"status": "ok", "counts": counts, "evidence_profiles": len(profiles)}))


if __name__ == "__main__":
    main()
