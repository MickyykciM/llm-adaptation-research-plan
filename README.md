# Forecasting Evidence-Induced Factual Failure

A decision-ready research plan and executable pilot scaffold for studying when an open-weight language model will make a factual error after a user challenge—and whether a selective verification gate can prevent harmful answer changes without blocking beneficial corrections.

## Recommendation

Pursue a tightly identified combination of Directions 1 and 3 from the project brief: **pre-response forecasting** is the prediction problem; **controlled evidence-sensitive revision** supplies the causal task environment and labels. Keep the Chameleon/Big Five mechanism study independent and run only its falsification pilot for now.

The central proposed contribution is not generic hallucination detection, a new flip-rate metric, or a generic personality direction. Each already has close prior art. The defensible question is:

> Can we predict, before the next answer is generated, whether a particular challenge/evidence context will induce a harmful factual error, distinguish evidence-evaluation failures from update-policy failures, and selectively trigger verification?

## What is in this repository

- [Full research plan](docs/RESEARCH_PLAN.md): decision table, three independent project designs, novelty assessment, hypotheses, controls, compute, and recommended paper framing.
- [48-hour and seven-day pilot](docs/PILOT_PROTOCOL.md): exact experimental cells, generation counts, acceptance gates, and schedule.
- [Literature map](docs/LITERATURE_MAP.md): primary sources and claim-to-source ledger through 2026-09-02.
- [Architecture](docs/ARCHITECTURE.md): reusable components and data flow; infrastructure is explicitly not claimed as a scientific contribution.
- [PreferenceDrift-Bench intake](docs/PREFERENCE_DRIFT_INTAKE.md): what the missing package could contribute and how to audit it without leakage.
- Machine-readable schemas, evidence templates, pilot configuration, and a standard-library Python scaffold with tests.

## Status and scope

This repository contains a **research design and starter implementation**, not completed experiments. It reports no empirical results and makes no unverified novelty claim. The prompt referenced an attached PreferenceDrift-Bench package, but no such package was present in the supplied materials; the plan therefore treats its value as conditional and provides an intake checklist.

Literature cutoff: **2026-09-02**. Peer-reviewed papers, preprints, and released artifacts are labeled separately.

## Quick start

Requires Python 3.11+ and no third-party packages for validation.

```powershell
python -m unittest discover -s tests -v
python scripts/validate_repo.py
python scripts/materialize_pilot_matrix.py --config configs/pilot.toml --output work/pilot_matrix.jsonl
```

The materializer creates identifiers and factor assignments only. It does not call a model or fabricate benchmark items.

## Reproducibility and data policy

Generated datasets, activations, model weights, and licensed third-party corpora are excluded from version control. Commit only schemas, templates, prompt hashes, manifests, aggregate metrics, and small auditable examples. Never commit credentials or raw user conversations.

## License

No license has been selected. All rights are reserved until the project owner chooses terms compatible with the eventual datasets and model licenses.
