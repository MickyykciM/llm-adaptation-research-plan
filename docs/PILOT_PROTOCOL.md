# Preregistered pilot protocol

## Decision objective

The pilot answers one go/no-go question:

> Does a model show enough separately measurable harmful drift and beneficial correction—and does prior-answer style causally alter either—to justify a full pre-response forecasting study?

No activation probe is the first milestone. A perfectly fitted probe on a weak, confounded, or parser-driven outcome would be a failed pilot.

## The next 48 hours: exact experiment

Run a matched behavioral viability screen on Qwen/Qwen2.5-7B-Instruct:

- 24 question families: 8 Bayesian, 8 mechanical, 8 fixed-passage grounded QA;
- 2 controlled initial states: correct and wrong;
- 2 decisive evidence conditions:
  - valid evidence supporting the gold answer;
  - invalid but plausible evidence supporting the distractor;
- 4 content-preserving prior-answer styles: neutral, confident, hedged, deferential;
- 2 rhetorical-pressure levels in the next user message: neutral and high;
- 1 fixed challenge-template family;
- 4 stochastic target continuations per cell at temperature .7, top-p .9.

Exact count:

~~~text
24 questions × 2 initial states × 2 evidence conditions
× 4 styles × 2 pressure levels × 1 template × 4 seeds
= 3,072 target next-answer generations
~~~

Use hand-authored or deterministic rewrites, not model-generated rewrites accepted without review. Within every style quartet, preserve the answer value, factual propositions, reasoning steps, and next user message. Match length as closely as possible; record exact token count and punctuation. Two reviewers, blinded to the target style, verify factual/propositional equivalence on all 192 unique rewritten prior answers or adjudicate disagreements.

Require the target model to return:

1. evidence validity: valid, invalid, or uncertain;
2. evidence relevance: relevant, irrelevant, or partial;
3. source reliability estimate from 0 to 100;
4. relation to its current answer: supports, contradicts, or neither;
5. final short answer and optional abstention.

The chain of thought is not requested or stored. A short structured rationale can be retained for auditing, but labels come from gold task mechanics.

### Primary outcomes

- Harmful drift in initially-correct/invalid-contradictory cells.
- Beneficial correction in initially-wrong/valid-corrective cells.
- Update Selectivity: beneficial-correction rate minus harmful-drift rate. This difference is useful but not novel; SycoBench-600 already defines the equivalent structure.
- Evidence-assessment accuracy for each evidence field.
- Evidence-evaluation versus update-policy failure: the latter means the structured evidence assessment is correct but the final answer remains wrong.

### Causal estimands

Estimate marginal risk differences for confident, hedged, and deferential versus neutral, separately in the harmful-drift and beneficial-correction cells. Use a mixed-effects logistic model with fixed effects for style, pressure, initial correctness, evidence condition, stage, and prespecified interactions; random intercepts for question family and seed. If convergence is poor, report paired cluster-bootstrap differences by question family. Do not interpret a surface-style effect as an internal mechanism.

### Viability gates

Proceed to the seven-day pilot only if:

- parser failure is at most 2%;
- content-equivalence disagreement is at most 5% after first review and resolved before analysis;
- harmful-drift rate is at least 10% in one invalid-evidence condition;
- beneficial-correction rate is at least 20% in one valid-evidence condition;
- neither outcome is explained almost entirely by one question family;
- evidence-assessment labels are mechanically unambiguous on at least 95% of reviewed cases.

Style need not have a significant effect to proceed. A null style effect would narrow the paper toward evidence-conditioned forecasting and rule out the proposed style-mediated causal claim.

## Seven-day confirmatory pilot

### Exact core matrix

The core block uses 60 question families:

- 20 Bayesian/probabilistic items with closed-form posterior targets;
- 20 arithmetic, logic, code, or table items with executable validators;
- 20 fixed-passage grounded-QA items with source spans frozen in the prompt.

Cross:

- 2 initial-answer states: correct/wrong;
- 8 evidence profiles;
- 2 rhetorical-pressure levels;
- 3 semantically equivalent challenge-template families;
- 4 stochastic continuations;
- 1 neutral prior-answer style.

~~~text
60 × 2 × 8 × 2 × 3 × 4 × 1 = 23,040 generations
~~~

This single branching design supports two labels:

- Task A, pre-challenge susceptibility: for each of 120 previous-response prefixes, average factual-error risk over the preregistered distribution of 8×2×3 challenge cells and 4 generation seeds, with equal cell weighting.
- Task B, post-challenge/pre-generation risk: for each of 5,760 unique challenged prompts, estimate soft factual-error risk from 4 repeated continuations; retain the first deterministic/greedy outcome as a secondary deployment-style hard label.

Four samples per Task B cell are noisy. The full study should increase a stratified subset to 20 or 50 continuations and report a sampling-budget ablation with beta-binomial or Wilson uncertainty.

### Eight evidence profiles

1. valid, decisive, supports gold, high-reliability source;
2. valid, decisive, supports gold, low-reliability source;
3. invalid, decisive-looking, supports distractor, high-reliability cue;
4. invalid, decisive-looking, supports distractor, low-reliability source;
5. valid, relevant, but insufficient;
6. ambiguous conflict between two independent, equally reliable pieces;
7. irrelevant evidence;
8. the same invalid evidence repeated three times and marked non-independent.

Rhetorical pressure is crossed separately. Confidence wording is never encoded as evidence validity or strength.

### Causal rewrite block

- 24 question families, 8 per stage;
- 2 initial states;
- 2 decisive evidence profiles;
- 4 prior-answer styles;
- 1 pressure level;
- 1 fixed template family;
- 4 seeds.

~~~text
24 × 2 × 2 × 4 × 1 × 1 × 4 = 1,536 generations
~~~

The exact next user message is fixed within each matched quartet. This block identifies the causal effect of surface stance conditional on content; it does not prove that any discovered activation is the mediator.

### Mitigation block

Lock 128 validation-selected, then test-held-out contexts spanning risk deciles and all four headline outcomes. Compare:

- evidence-verification gate;
- self-consistency plus deterministic evidence checker.

With 2 intervention arms and 4 seeds:

~~~text
128 × 2 × 4 = 1,024 generations
~~~

Also evaluate already-generated no-intervention controls, random triggering at matched coverage, always-on verification, prompt-only triggering, and an oracle risk ranking. Do not tune the threshold on test outcomes.

### Total

~~~text
core 23,040 + causal 1,536 + mitigation 1,024 = 25,600
~~~

At an assumed mean of 80 output tokens, this is about 2.05 million output tokens, plus prompt processing and intervention overhead. A 7B BF16 reference run should fit on a 24 GB GPU at microbatch 1; throughput depends strongly on context length, attention capture, and hardware. Budget approximately 12–40 single-GPU hours for generation/capture, then measure rather than report that range as achieved compute. Store final-token residual states and online attention summaries only; full attention tensors can make the pilot infeasible.

## Split protocol

Allocate the 60 question families 36/12/12 to train/validation/test, stratified as 12/4/4 per stage. All paraphrases, initial states, evidence versions, styles, pressures, and seeds for a question stay together.

Challenge-template generalization requires a second grouping constraint. Use either:

- nested evaluation: train on two template families and test the third within train/validation question families, then confirm on locked question-held-out cells; or
- a strict Cartesian quarantine in which every question and template family in the confirmatory test is unseen during fitting.

Do not randomly row-split the 5,760 prompts. Fit feature selection, PCA, scaling, probability calibration, and thresholds inside training folds. OOD reports should hold out stage/domain and template family; any cross-model result is a later extension.

## Forecasting models and comparisons

### Task A

Predict soft susceptibility using only the previous assistant response and pre-existing question context—never the next user message. Compare:

1. base rate by stage;
2. question identity/difficulty embedding and initial correctness;
3. prior-response surface features: length, hedging, certainty, apology, agreement, deference;
4. semantic stance/consistency;
5. prior-response logits/entropy/margin;
6. layerwise residual states;
7. expensive counterfactual-continuation estimate as an upper baseline.

### Task B

After adding the user challenge but before target generation, compare nested blocks:

1. stage/difficulty/initial correctness;
2. exact challenge/evidence factors and prompt text;
3. Task-A risk and prior-response surface features;
4. prompt logits/entropy/answer margin;
5. post-challenge residuals;
6. cross-turn residual deltas;
7. attention grounding/concentration/transition summaries.

The primary result is incremental held-out value over factors 1–2, not a raw AUROC. Report AUROC, area under precision–recall curve, Brier score, log loss, expected calibration error, calibration slope/intercept, and risk-coverage curves. Compare nested models by clustered bootstrap confidence intervals and out-of-fold paired loss differences. Correct multiple mechanistic comparisons with Benjamini–Hochberg FDR; use confirmatory hypotheses for a small preregistered set.

## Seven-day schedule

### Day 1 — labels before models

Freeze the construct definitions, evidence profiles, schemas, 24-item 48-hour subset, answer parser, and content-equivalence rubric. Audit all gold answers and normative posteriors.

### Day 2 — behavioral viability

Run the 3,072-generation screen. Blind-review parser failures and equivalence. Produce the four-outcome table by stage, style, and pressure. Apply the viability gates.

### Day 3 — full item bank and leakage audit

Build and double-check all 60 families and three template families. Freeze question-group splits and prompt hashes. Confirm that no normalized stem/entity/template crosses a prohibited split.

### Day 4 — core branching

Run the 23,040 core generations with deterministic logs and manifest. Capture lightweight prompt logits and final-token residuals; sample-check 5% of outputs before continuing.

### Day 5 — baselines and calibrated probes

Fit question/difficulty, surface, prompt-only, residual, and cross-turn models with grouped nested validation. Compute Task A and Task B soft labels and sampling uncertainty. Do not inspect test performance while selecting layers or thresholds.

### Day 6 — causal and mitigation blocks

Run 1,536 rewrite generations and 1,024 mitigation generations. Estimate paired style effects and cost/coverage curves. Separate evidence-evaluation from update-policy failures.

### Day 7 — locked analysis and decision

Run the frozen test analysis once. Produce aggregate tables, calibration plots, failure audit, compute/latency report, and a one-page continue/pivot/stop memo. Archive configs, hashes, software versions, and exclusions.

## Deliverables after one week

- validated 60-family item set and eight evidence profiles;
- 25,600-row trial table with no raw hidden tensors in Git;
- Task A and B grouped-OOD baseline table;
- calibration and risk-coverage plots;
- causal rewrite effect table;
- mitigation factuality/correction/cost table;
- error-decomposition audit;
- reproducibility manifest and a documented go/no-go decision.

No paper-level mechanism claim should be made from the pilot. A full study would add 20–50 continuation labels on a stratified subset, one held-out model family, human validation for grounded QA, candidate-head confirmation on a fresh split, and causal patching/ablation.
