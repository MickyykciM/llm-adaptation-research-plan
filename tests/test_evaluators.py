from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.evaluators.mechanical import exact_match, numeric_match
from adaptlab.evaluators.personality import score_trait, trait_shift


class EvaluatorTests(unittest.TestCase):
    def test_normalized_exact_match(self) -> None:
        self.assertTrue(exact_match("  PARIS. ", "paris"))
        self.assertTrue(numeric_match("1,024", "1024"))

    def test_reverse_scoring(self) -> None:
        score = score_trait({"p": 5, "r": 1}, ["p"], ["r"])
        self.assertEqual(score, 10)
        self.assertEqual(trait_shift(30, 34), 4)


if __name__ == "__main__":
    unittest.main()
