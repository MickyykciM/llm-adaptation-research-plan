from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.splits import assert_group_disjoint, stable_group_split
from adaptlab.types import (
    EvidenceRecord,
    EvidenceRelation,
    EvidenceRelevance,
    EvidenceValidity,
    TrialRecord,
)


class SplitAndLeakageTests(unittest.TestCase):
    def test_split_is_stable(self) -> None:
        ids = [f"q-{index}" for index in range(100)]
        assignments = stable_group_split(ids)
        self.assertEqual(assignments, stable_group_split(reversed(ids)))
        self.assertEqual(list(assignments.values()).count("train"), 60)
        self.assertEqual(list(assignments.values()).count("validation"), 20)
        self.assertEqual(list(assignments.values()).count("test"), 20)

    def test_group_leakage_is_rejected(self) -> None:
        rows = [
            {"split": "train", "question": "q1", "template": "t1"},
            {"split": "test", "question": "q1", "template": "t2"},
        ]
        with self.assertRaises(ValueError):
            assert_group_disjoint(rows, ("question",))

    def test_target_activation_leakage_is_rejected(self) -> None:
        evidence = EvidenceRecord(
            evidence_id="e",
            text="fixture",
            validity=EvidenceValidity.VALID,
            relevance=EvidenceRelevance.RELEVANT,
            diagnostic_strength=1.0,
            source_reliability=1.0,
            relation_to_gold=EvidenceRelation.SUPPORTS_GOLD,
            rhetorical_pressure="neutral",
        )
        trial = TrialRecord(
            trial_id="x",
            question_family_id="q",
            stage="mechanical",
            challenge_template_family="t",
            initial_answer="wrong",
            initial_correct=False,
            previous_style="neutral",
            evidence=evidence,
            metadata={"target_hidden_states": [1, 2, 3]},
        )
        with self.assertRaises(ValueError):
            trial.validate_pre_response_features()


if __name__ == "__main__":
    unittest.main()
