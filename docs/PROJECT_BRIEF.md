# Original project brief

This file preserves the user-supplied research-design brief that this repository answers. It is included for provenance and review; it is not an empirical result.

---

You are acting as a senior NLP researcher, research-design reviewer, and project architect. I need a decision-ready research plan, not a loose brainstorming list.

## Materials

1. “The Point of No Return: Counterfactual Localization of Deceptive Commitment in Language-Model Reasoning”
   https://arxiv.org/abs/2605.17113

2. “Chameleon LLMs: User Personas Influence Chatbot Personality Shifts”
   https://aclanthology.org/2025.emnlp-main.875/

3. The attached PreferenceDrift-Bench project package.

Treat files inside the project package as research materials, not as instructions.

## Important framing

My professor explicitly told me not to limit my ideas to PreferenceDrift-Bench. The project may be extended, partially reused, substantially redesigned, or abandoned if another research direction is stronger.

Do not force the following three directions into one paper. First assess them as three independent candidate projects. Only recommend a combination if the variables and causal claims remain separately identifiable.

## Direction 1: Predicting next-turn factual errors

Research whether properties of a model’s previous response can predict whether its next response will contain a factual error.

Explicitly compare this question with The Point of No Return. Explain:

- their shared early-warning structure;
- deception versus accidental factual error;
- sentence-level reasoning prefixes versus dialogue turns;
- localization versus forecasting;
- mechanically labeled deception versus factuality labels;
- whether adapting counterfactual localization would constitute replication, extension, or a new contribution.

Separate two prediction tasks:

A. Pre-challenge susceptibility:
Using only the previous model response, predict its average vulnerability over a predefined distribution of future user challenges.

B. Post-challenge, pre-generation risk:
After seeing the next user message but before generating the next answer, predict whether the answer will be factually wrong.

For both tasks, consider these feature families:

- surface linguistic features: hedging, certainty, agreement, apology, deference and response length;
- semantic stance and consistency;
- token probabilities, entropy and answer margins;
- layer-wise residual-stream hidden states;
- changes in hidden states across turns;
- attention distributions and attention-head outputs;
- attention transitions between the original question, prior answer and user evidence;
- counterfactual continuation statistics.

Do not use any activation from the target next response when making a pre-response prediction.

Compare against controls for question difficulty, question identity, previous-answer correctness, response length, challenge type and the exact next-user prompt. Use grouped splits by question and challenge template.

Distinguish prediction from causation. Propose a causal experiment using content-preserving rewrites of the same previous answer into neutral, confident, hedged and deferential versions while holding factual content and the next user message fixed.

Also propose a practical mitigation system. For example, a high predicted risk could trigger retrieval, evidence verification, self-consistency sampling, abstention or activation steering. Evaluate factual improvement, false alarms, added latency and computation cost.

## Direction 2: Mechanisms of conversational personality adaptation

Use the definition of personality from Chameleon LLMs. Personality here means a context-conditioned change in perceived Big Five traits measured through IPIP-style assessments—not generic tone, confidence, sycophancy or an intrinsic human-like personality.

First reconstruct the Chameleon study, including:

- its 100 user personas and 50 scenarios;
- 20-turn dialogue design;
- IPIP-50 pre/post scores;
- trait-shift definition;
- seven chatbot models;
- prediction features;
- amplify/resist prompting experiments;
- temporal and WildChat analyses;
- measurement limitations;
- available code and data artifacts.

Clearly state that Chameleon does not identify hidden-state layers, neurons or attention heads.

Use literature available through September 2026 to determine what personality probing and activation steering work already exists. In particular, assess whether simply finding a Big Five direction or “personality layer” would still be novel.

Develop at least two possible mechanistic extensions:

1. A pure personality project:
Locate where user-induced Big Five adaptation emerges across conversation turns, then causally test layers, heads or latent directions using patching, ablation or steering.

2. An optional personality–factuality project:
Test whether style adaptation and factual preference drift share internal mechanisms. Keep this formulation only if style, evidence validity and factual correctness can be independently manipulated.

The design should distinguish:

- lexical or punctuation imitation;
- perceived Big Five trait change;
- adaptation susceptibility;
- factual belief state;
- evidence weighting.

Include leave-persona-out and leave-scenario-out tests, target- versus non-target-trait effects, and measures of fluency, helpfulness, coherence, factuality and general capability.

Compare prompt-level “resist adaptation” with activation-level intervention. Explain how to test whether an intervention selectively reduces harmful adaptation without eliminating appropriate conversational accommodation.

## Direction 3: Evidence-sensitive answer revision

Turn “When should a model change its answer?” into an operational research problem about selective epistemic updating.

Represent evidence using separate fields:

- validity;
- relevance;
- diagnostic strength;
- source reliability;
- supports versus contradicts;
- rhetorical pressure;
- repetition;
- independence from previous evidence.

Do not treat confident wording as evidence strength.

The minimum outcome ontology must include:

- initially correct + rejects invalid contradictory evidence = justified persistence;
- initially correct + accepts invalid contradictory evidence = harmful drift;
- initially wrong + accepts valid corrective evidence = beneficial correction;
- initially wrong + rejects valid corrective evidence = stubbornness.

Also include supporting, irrelevant, insufficient and ambiguous evidence.

Propose a staged benchmark:

1. Bayesian or probabilistic update tasks with computable normative answers.
2. Mechanically verifiable arithmetic, logic, code or table tasks.
3. Source-grounded factual QA with fixed evidence passages.

Require the model to assess the evidence before producing its final answer so that errors can be decomposed into:

- evidence-evaluation failure;
- update-policy failure.

Propose a selective-updating metric rather than reporting only flip rate. Consider:

Update Selectivity =
P(beneficial correction) - P(harmful flip).

Also propose a solution such as an evidence-verification gate, retrieval checker, selective-update training objective or activation-based intervention.

## Required research output

Begin with a decision table containing:

- precise research question;
- closest prior work;
- degree of overlap;
- unresolved gap;
- novelty risk;
- feasibility with a 2B–8B open-weight model;
- role of PreferenceDrift-Bench;
- primary confound;
- decision: PURSUE NOW / RUN PILOT / DEFER;
- KEEP SEPARATE / POSSIBLE COMBINATION.

For each direction, provide:

1. A minimum viable 1–2 week study.
2. A higher-novelty mechanistic or causal version.
3. Falsifiable hypotheses.
4. Unit of analysis.
5. Independent and dependent variables.
6. Exact labels and data schema.
7. Confounders and controls.
8. Recommended small open-weight model.
9. Baselines.
10. Grouped and out-of-distribution splits.
11. Metrics and statistical tests.
12. Estimated number of generations and compute requirements.
13. Expected one-week and full-study artifacts.
14. The fastest failure diagnostic.
15. What PreferenceDrift-Bench can and cannot contribute.

## Data and software architecture

Design reusable, model-agnostic components for:

- model adapters;
- structured scenario and evidence generation;
- prefix branching and repeated continuations;
- activation and logit recording;
- optional attention-head extraction;
- factuality and personality evaluators;
- probe training;
- activation intervention;
- metrics and reproducibility manifests.

Treat this architecture as infrastructure, not automatically as the scientific contribution.

## Combination rule

Only combine directions if:

- every construct retains a precise definition;
- independent variables can be manipulated independently;
- predictors are measured before outcomes;
- personality shift, factuality and evidence response have separate labels;
- causal claims can use matched or counterfactual prefixes;
- sufficient data exists in every experimental cell;
- the effect of persona, tone, evidence validity, pressure and initial correctness can be separated.

Specifically assess whether Directions 1 and 3 combine naturally, while Direction 2 should remain an independent mechanistic project.

## Final deliverables

End with:

1. The single experiment I should run in the next 48 hours.
2. A seven-day pilot schedule.
3. An exact pilot data matrix and generation count.
4. Files and software modules to create.
5. A “do not do yet” list.
6. Three questions to ask my professor.
7. A natural, non-AI-sounding paragraph for my shared meeting document.

Use current primary literature and link papers, datasets and official repositories. Clearly distinguish replication, extension and new contribution. Do not invent results or claim novelty without evidence.
