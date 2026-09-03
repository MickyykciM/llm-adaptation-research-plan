# PreferenceDrift-Bench intake and reuse boundary

## Current status

The supplied materials referenced an attached PreferenceDrift-Bench project package, but the attachment contained only the research brief. No code, data, schemas, prompts, results, license, or model outputs were available. Consequently, this plan makes no claim about the package’s contents or quality.

PreferenceDrift-Bench is optional. The recommended project must remain valid if the package is unusable.

## Intake checklist

Before reuse, inventory:

1. repository commit, archive hash, provenance, and license;
2. task sources and any downstream-use restrictions;
3. prompt templates, model/chat-template revisions, decoding settings, and seeds;
4. unit of analysis and whether multiple rows share a question, persona, or template;
5. initial-answer correctness and how it was established;
6. challenge/evidence text and whether evidence validity is independently verifiable;
7. whether confidence, evidence strength, source reliability, pressure, repetition, and dependence are separable;
8. raw versus derived labels and evaluator code;
9. target-response activation leakage or post-outcome features;
10. train/test contamination, duplicated paraphrases, and preprocessing fitted before splitting;
11. parser failures, exclusions, reruns, missing cells, and human adjudication;
12. whether released counts reconcile with the paper/report.

Run schema migration only after this audit. Preserve original row IDs and hashes.

## What it could contribute

If licensed and structurally suitable, it may provide:

- candidate question families and dialogue/challenge templates;
- prior assistant answers and controlled revision trajectories;
- style or pressure manipulations;
- evaluator code and manually reviewed factuality labels;
- realistic failure examples for external validation;
- a comparison benchmark for the four-outcome ontology.

Treat these as candidate inputs, not ground truth by reputation.

## What it cannot contribute without redesign

It cannot establish the proposed causal or forecasting claims if it lacks:

- a feature snapshot before the target answer;
- both initial-correct and initial-wrong cells;
- independently labeled valid and invalid evidence;
- distinct evidence validity, relevance, strength, reliability, pressure, repetition, and independence;
- content-preserving answer-style counterfactuals;
- repeated continuations for a soft risk target;
- question- and template-grouped splits;
- explicit evidence assessment before final revision.

Retrofitting prose labels into these constructs would create measurement error, not new evidence.

## Reuse decision rule

- **Reuse directly** only for cells whose provenance, temporal boundary, factors, and labels pass the schema.
- **Transform with audit trail** when a deterministic mapping is possible and validated on a double-coded sample.
- **Use only for external validation** when factors are entangled but outcomes are reliable.
- **Discard** when license/provenance is unclear, target leakage is unavoidable, or correctness/evidence validity cannot be verified.

The first professor question should therefore be whether the package was omitted accidentally and whether a versioned, licensed copy can be shared.
