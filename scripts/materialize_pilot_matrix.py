"""Write the preregistered factor grid without creating prompts or outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptlab.branching import generation_counts, iter_factor_rows, load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(ROOT / "configs" / "pilot.toml"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8") as handle:
        for row in iter_factor_rows(config):
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            count += 1
    expected = generation_counts(config)["total"]
    if count != expected:
        raise RuntimeError(f"materialized {count}; expected {expected}")
    print(json.dumps({"output": str(output), "rows": count}))


if __name__ == "__main__":
    main()
