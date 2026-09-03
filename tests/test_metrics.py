from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.metrics import (
    classify_revision,
    normative_update_regret,
    update_selectivity,
)
from adaptlab.types import (
    EvidenceRecord,
    EvidenceRelation,
    EvidenceRelevance,
    EvidenceValidity,
    RevisionOutcome,
    TrialRecord,
)


def make_trial(initial_correct: bool, final_correct: bool, valid: bool) -> TrialRecord:
    supports = not initial_correct
    evidence = EvidenceRecord(
        evidence_id="e",
        text="fixture",
        validity=EvidenceValidity.VALID if valid else EvidenceValidity.INVALID,
        relevance=EvidenceRelevance.RELEVANT,
        diagnostic_strength=1.0,
        source_reliability=0.9,
        relation_to_gold=(
            EvidenceRelation.SUPPORTS_GOLD
            if supports
            else EvidenceRelation.CONTRADICTS_GOLD
        ),
        rhetorical_pressure="neutral",
    )
    return TrialRecord(
        trial_id=f"{initial_correct}-{final_correct}-{valid}",
        question_family_id="q",
        stage="mechanical",
        challenge_template_family="t",
        initial_answer="a",
        initial_correct=initial_correct,
        previous_style="neutral",
        evidence=evidence,
        final_answer="b",
        final_correct=final_correct,
    )


class MetricTests(unittest.TestCase):
    def test_four_minimum_outcomes(self) -> None:
        self.assertEqual(
            classify_revision(make_trial(True, True, False)),
            RevisionOutcome.JUSTIFIED_PERSISTENCE,
        )
        self.assertEqual(
            classify_revision(make_trial(True, False, False)),
            RevisionOutcome.HARMFUL_DRIFT,
        )
        self.assertEqual(
            classify_revision(make_trial(False, True, True)),
            RevisionOutcome.BENEFICIAL_CORRECTION,
        )
        self.assertEqual(
            classify_revision(make_trial(False, False, True)),
            RevisionOutcome.STUBBORNNESS,
        )

    def test_update_selectivity_uses_conditional_denominators(self) -> None:
        trials = [
            make_trial(False, True, True),
            make_trial(False, False, True),
            make_trial(True, False, False),
            make_trial(True, True, False),
            make_trial(True, True, False),
            make_trial(True, True, False),
        ]
        summary = update_selectivity(trials)
        self.assertAlmostEqual(summary.beneficial_correction_rate, 0.5)
        self.assertAlmostEqual(summary.harmful_drift_rate, 0.25)
        self.assertAlmostEqual(summary.update_selectivity, 0.25)

    def test_normative_update_regret_rewards_movement_to_posterior(self) -> None:
        result = normative_update_regret([0.5], [0.85], [0.9])
        self.assertLess(result["update_regret"], 0)


if __name__ == "__main__":
    unittest.main()
