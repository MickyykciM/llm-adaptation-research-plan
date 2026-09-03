"""Small CLI for design validation."""

from __future__ import annotations

import argparse
import json

from .branching import generation_counts, load_config


def main() -> None:
    parser = argparse.ArgumentParser(prog="adaptlab")
    subparsers = parser.add_subparsers(dest="command", required=True)
    count_parser = subparsers.add_parser("count", help="count preregistered generations")
    count_parser.add_argument("config")
    args = parser.parse_args()

    if args.command == "count":
        print(json.dumps(generation_counts(load_config(args.config)), indent=2))


if __name__ == "__main__":
    main()
