from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.branching import generation_counts, iter_factor_rows, load_config


class BranchingTests(unittest.TestCase):
    def test_exact_generation_count(self) -> None:
        config = load_config(ROOT / "configs" / "pilot.toml")
        self.assertEqual(
            generation_counts(config),
            {"core": 23040, "causal": 1536, "mitigation": 1024, "total": 25600},
        )

    def test_materialized_ids_are_unique(self) -> None:
        config = load_config(ROOT / "configs" / "pilot.toml")
        ids = [row["trial_id"] for row in iter_factor_rows(config)]
        self.assertEqual(len(ids), 25600)
        self.assertEqual(len(set(ids)), 25600)


if __name__ == "__main__":
    unittest.main()
