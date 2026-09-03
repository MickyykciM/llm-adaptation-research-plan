# Software and data architecture

This architecture makes the study auditable and reusable. It is infrastructure, not automatically a scientific contribution.

## Design principles

1. Capture forecast features at a named temporal boundary and reject target-response activations.
2. Keep question content, evidence semantics, rhetorical pressure, answer style, and sampling seed as separate fields.
3. Branch matched continuations from an immutable prefix and store a prompt hash.
4. Prefer mechanical labels; quarantine judge-labeled cases and report judge sensitivity.
5. Group by question family and challenge-template family before fitting any preprocessing step.
6. Pin model and dataset revisions; preserve compact manifests instead of committing large artifacts.

## Data flow

~~~text
question family + gold/distractor
            |
            v
scenario/evidence constructor ----> schema validation
            |
            v
immutable dialogue prefix --------> SHA-256 + split assignment
       |                |
       | Task A         | append fixed challenge/evidence
       v                v
previous-turn       Task B prompt boundary
features                |
       |                +--> logits/residual/attention summaries
       +----------------+
            |
            v
calibrated risk model ----> selective mitigation gate
            |                         |
            v                         v
repeated target generations <--- verification/self-consistency
            |
            v
mechanical factuality + evidence-appraisal evaluation
            |
            v
outcome ontology, calibration, selectivity, cost, mixed-effects analysis
~~~

## Components

### Model adapters

The adapter protocol in src/adaptlab/adapters/base.py separates prompt-only capture from generation. Each concrete adapter must expose model ID and immutable revision, tokenizer/chat-template version, decoding parameters, token IDs, latency, and capture boundary. The first implementation should target Hugging Face Transformers and Qwen2.5-7B-Instruct. A vLLM adapter may be added for behavioral throughput, but Transformers remains the reference for activation hooks.

### Scenario and evidence generation

Items conform to schemas/item.schema.json. Evidence conforms to schemas/evidence.schema.json; validity, relevance, diagnostic strength, source reliability, relation to the gold answer, rhetoric, repetition, and dependence never share one overloaded field. data/templates/evidence_profiles.json defines the eight pilot profiles. Generators must emit provenance and version, then pass a deterministic verifier.

### Prefix branching and repeated continuations

Persist one canonical message list per prefix. Task A captures after the prior assistant answer. Task B appends the challenge and captures before target decoding. Continuations vary only the preregistered seed. The factor-grid code in src/adaptlab/branching.py counts and materializes assignments; it intentionally does not invent questions or outputs.

### Activation and logit recording

Record:

- prompt token probabilities, entropy, answer-option margin when options exist;
- last-token and span-pooled residuals at every layer;
- current-minus-previous-turn and current-minus-mean-of-prior-turn deltas;
- online attention summaries for tokens in original question, prior answer, evidence, and rhetoric spans;
- only preregistered head outputs after the pilot identifies candidates.

Do not store full attention matrices by default. Capture final-token all-layer residuals in BF16, summarize attention online, and record tensor shape/dtype/device. Never admit a feature computed from target response tokens into a pre-response probe.

### Evaluators

src/adaptlab/evaluators/mechanical.py handles strict normalization for closed-form answers. Bayesian tasks use exact posteriors from a versioned generator. Code/logic/table tasks use executable validators. Fixed-passage QA uses answer spans plus a blinded adjudication queue for genuine ambiguity. Evidence assessment is scored separately from the final answer.

src/adaptlab/evaluators/personality.py implements only IPIP-style scoring. It does not imply intrinsic model personality. A Direction 2 implementation would add randomized item order, reverse-key reliability checks, open-ended behavioral rubrics, lexical controls, and independent raters.

### Probes

Every feature has a descriptor naming source turn and capture boundary. Baselines progress in this order:

1. difficulty/question metadata and previous correctness;
2. surface features and response length;
3. exact challenge/evidence fields;
4. prompt probabilities and entropy;
5. residual states and cross-turn deltas;
6. attention summaries;
7. counterfactual continuation statistics as an expensive upper baseline.

Fit scalers/PCA/calibrators within training folds only. Compare nested models to measure the incremental value of prior-response stance and internal features.

### Interventions

The initial gate in src/adaptlab/interventions/gates.py triggers an evidence-verification pass or self-consistency only above a validation-set threshold. Activation steering is deferred until a predictive direction survives causal tests. Evaluate paired factual gain, beneficial-correction retention, false-alarm rate, coverage, latency, token count, and a preregistered cost utility.

### Metrics and manifests

src/adaptlab/metrics.py provides the four required outcomes, Update Selectivity, normative update regret, calibration, and evidence-evaluation versus update-policy decomposition. This implementation does not claim Update Selectivity as novel; SycoBench-600 already uses the same difference structure.

Each run manifest should include:

- git commit and dirty-state flag;
- exact configuration hash;
- model/tokenizer/chat-template revisions;
- source URIs, licenses, and dataset hashes;
- prompt/evaluator versions;
- seeds and deterministic settings;
- hardware, software, precision, and attention implementation;
- exclusions, parser failures, reruns, and human adjudications.

## Repository boundaries

- configs/: preregistered factors and capture policy.
- data/templates/: small, reviewable templates only.
- data/raw/, data/processed/: local and gitignored.
- schemas/: machine-readable contracts.
- src/adaptlab/: model-agnostic experiment logic.
- scripts/: entry points and offline validation.
- tests/: leakage, count, metric, and normalization checks.
- results/: compact aggregate artifacts after real runs.

Before any full experiment, add concrete Transformers hooks, validators for each task family, a model-independent prompt renderer, content-rewrite equivalence tests, and a locked analysis script. Those missing components are deliberate: this repository is a research-plan scaffold, not a falsely complete experimental system.
