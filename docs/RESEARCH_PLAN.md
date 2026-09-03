# Decision-ready research plan

| Candidate | Precise research question | Closest prior work | Overlap | Unresolved gap | Novelty risk | 2B–8B feasibility | PreferenceDrift-Bench role | Primary confound | Decision | Combination |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Next-turn factual-risk forecasting | Before the next answer, can we estimate challenge-induced factual-error risk beyond question difficulty, initial correctness, and the exact challenge—and does prior-answer stance add causal value? | [Not Just RLHF](https://arxiv.org/html/2605.12991), [Pre-Generation Hallucination Detection](https://arxiv.org/abs/2606.21917), [Query-Level Uncertainty](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3a07c3a67cfe50d3236b71fb674c7f30-Abstract-Conference.html), [FactCheckmate](https://aclanthology.org/2025.findings-emnlp.663/), [Point of No Return](https://arxiv.org/abs/2605.17113) | High for generic Task B; medium for distribution-average Task A; lower for rigorously controlled incremental cross-turn risk | Separate pre-challenge susceptibility from post-challenge risk; quantify excess risk due to prior answer/challenge; grouped template OOD; matched stance causality; costed selective mitigation | **High** if sold as “pre-generation detection”; **moderate** under the narrow framing | High with Qwen2.5-7B; activation capture fits one 24 GB GPU with careful summaries | Possible item/template source or external test after audit; not required | Baseline knowledge/difficulty masquerading as susceptibility; question/template leakage | **PURSUE NOW**, but only with narrow claim | **POSSIBLE COMBINATION with 3** |
| 2. Conversational Big Five adaptation mechanisms | Where across turns/layers does user-induced, context-conditioned perceived Big Five shift emerge, and can it be selectively suppressed without removing appropriate accommodation? | [Chameleon LLMs](https://aclanthology.org/2025.emnlp-main.875/), [Personality Alignment](https://arxiv.org/abs/2408.11779), [Neuron-based Personality Trait Induction](https://arxiv.org/abs/2410.12327), [Activation-Space Personality Steering](https://aclanthology.org/2026.eacl-long.300/), [PERSONA](https://arxiv.org/abs/2602.15669) | High for static Big Five directions/layers/heads/neurons; lower for causal turn-resolved user-induced adaptation | Matched natural dialogue, emergence over turns, static-versus-induced subspaces, causal mediation beyond lexical imitation, selective resistance | **High** for “find a personality layer”; **moderate** for user-induced causal dynamics | Behavioral pilot high; full head/circuit search moderate but feasible on 7B | At most dialogue/style templates unless it contains validated Big Five manipulations | IPIP prompt instability and lexical imitation being mistaken for personality | **RUN PILOT** | **KEEP SEPARATE** |
| 3. Evidence-sensitive answer revision | Can a model assess evidence attributes, update in the warranted direction and magnitude, and expose whether failures arise in appraisal or update policy? | [Resist and Update](https://arxiv.org/abs/2607.12985), [DeReLab](https://arxiv.org/abs/2608.30413), [SycoBench-600](https://aclanthology.org/2026.findings-acl.1759/), [BASIL](https://arxiv.org/abs/2508.16846), [Balanced Persuasion Training](https://aclanthology.org/2025.naacl-long.412/) | Very high for Bayesian reliability×pressure, activation intervention, accept/resist balance, and appraisal | Prospective risk forecasting; appraisal-versus-policy causality; correlated/repeated/irrelevant/ambiguous multi-evidence; nonbinary magnitude; mechanical and fixed-passage transfer | **Very high** as a standalone contribution; **moderate–high** only as controlled substrate for Direction 1 | Very high behaviorally; high for prompt gate; moderate for activation intervention | Candidate examples/evaluators if labels can be remapped; optional | Validity, rhetoric, source cues, and diagnostic strength being entangled | **RUN PILOT** as task substrate; do not lead with it as new benchmark/mechanism | **POSSIBLE COMBINATION with 1** |

## Status, cutoff, and recommendation

This document is a prospective design. It contains **no empirical results**. It distinguishes established prior results, design choices, and hypotheses. The primary-literature search cutoff is **2026-09-02**; peer-reviewed papers and preprints are identified in the [literature map](LITERATURE_MAP.md). Absence of a paper from a bounded search is not proof of novelty.

The strongest project is **Forecasting Evidence-Induced Factual Failure**: combine Direction 1’s two pre-response prediction tasks with Direction 3’s controlled evidence-revision environment. The variables remain separately identifiable:

- factuality is a mechanically scored outcome;
- evidence validity, relevance, diagnosticity, reliability, rhetoric, repetition, and dependence are separate manipulations;
- prior-answer style is changed only in a matched causal block;
- prediction features are measured before the outcome;
- evidence appraisal is labeled separately from final answer revision.

Direction 3 is therefore the labeled experimental substrate, not a second vague contribution. The proposed scientific claim is incremental, cross-turn forecasting and selective mitigation—not the software architecture, generic pre-generation detection, the four-cell ontology, or the Update Selectivity difference.

Direction 2 should remain independent. Personality is an IPIP-style perceived-trait shift, not factual belief, evidence weighting, confidence, tone, or sycophancy. Combining it now would multiply conditions, weaken construct validity, and make mediation underpowered.

The prompt referenced a PreferenceDrift-Bench package, but no package was present. Its contribution is conditional; see [the intake protocol](PREFERENCE_DRIFT_INTAKE.md).

## Common model and measurement choices

Use [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) as the first open-weight model. It is within the 2B–8B constraint, has an Apache-2.0 model repository, exposes all internals, appears in Chameleon, and is close to models used in recent pre-generation probes. Pin the exact revision and tokenizer/chat template. Use BF16 for causal mechanism work; 4-bit quantization is acceptable only for an explicitly labeled behavioral smoke test.

Use temperature .7, top-p .9, fixed max tokens, and four preregistered seeds in the pilot. Report greedy correctness separately from stochastic risk. Do not call a probability an intrinsic belief without a task-specific operational definition.

# Direction 1 — predicting next-turn factual errors

## Position relative to The Point of No Return

[The Point of No Return](https://arxiv.org/abs/2605.17113) and Direction 1 share an early-warning structure: both study a conditional probability of an undesirable future outcome given a prefix; both can estimate that probability using repeated counterfactual continuations; both ask whether prefix representations predict risk; and both motivate an intervention before the outcome.

They differ in five decisive ways:

| Dimension | Point of No Return | Proposed Direction 1 |
|---|---|---|
| Phenomenon | Strategic, environment-labeled deceptive behavior; the paper cautions that outcome labels do not prove intent | Accidental factual error or harmful answer revision under controlled evidence |
| Unit/boundary | Sentence prefix inside a reasoning trajectory | Public dialogue turns: after prior answer for Task A; after next user message but before next answer for Task B |
| Temporal claim | Localizes a risk jump after the candidate sentence is included | Forecasts an unseen next answer; Task A also precedes the unseen challenge |
| Label | Oracle/environment mechanics classify a trajectory as deceptive/honest | Mechanical correctness, evidence fields, and repeated-continuation error rate |
| Causal target | Patch honest branch activations to reduce likelihood of an exact deceptive commitment sentence | Manipulate prior-answer stance or evidence appraisal, then measure next-answer factuality and selective updating |

PONR studies five synthetic environments—Bluff, Maze Guide, Investment Advisor, Car Sales, and Offer Negotiation—and four reasoning models. For each sentence prefix it samples 50 continuations, estimates deception probability, searches for an earliest probability crossing, and labels a deceptive juncture when the probability jump exceeds .3. Its features include TF-IDF, last-token residual states, residual differences, and attention grounding/concentration/transition summaries. Leave-one-environment-out attention-plus-PCA AUROC is reported between .701 and .755 across the four models. It then patches sparse attention-head sets from matched honest/deceptive branches and reports lower teacher-forced likelihood of the target commitment sentence; a small Qwen-7B steering experiment also lowers generated deception. These are PONR’s reported results, not results of this project.

Adapting its counterfactual localization code to reproduce deception boundaries would be **replication**. Keeping the localization method but relabeling continuations for factuality would be a **construct/domain extension**, explicitly anticipated in PONR’s limitations. The proposed dialogue design becomes a plausibly new contribution only through the two temporal tasks, controlled challenge-induced excess risk, question/template-held-out evaluation, matched stance manipulation, and costed gate. Even then, novelty is bounded by closer pre-generation work below.

The PONR release has material artifact caveats: its Hugging Face dataset is public, but no corresponding code repository was located; paper-level scale descriptions do not fully reconcile; and the dataset viewer was not functioning during review. Do not inherit its thresholds or call its mechanism behaviorally causal without revalidation.

## Closest novelty threats

- [Not Just RLHF](https://arxiv.org/html/2605.12991) Appendix C.5 already predicts a pressured correct-to-wrong yield before the answer from Llama residual states, reporting pooled AUC as high as .925. It is the closest direct Task B collision. Its setting is easy/preknown multiple-choice questions with a fixed wrong option; repeated pressure variants appear row-split rather than question-grouped; it does not isolate prior free-form answer properties, Task A, evidence validity, or calibrated incremental risk. This project is an extension, not a first pre-onset yield detector.
- [Pre-Generation Hallucination Detection via Soft-Target Attention Probing](https://arxiv.org/abs/2606.21917) already learns a prompt-token attention pooler against empirical error rates from ten stochastic answers. It directly occupies generic soft-risk Task B. Its artifact link and some model reporting were not independently verifiable at cutoff.
- [Query-Level Uncertainty](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3a07c3a67cfe50d3236b71fb674c7f30-Abstract-Conference.html) estimates correctness before generation and demonstrates adaptive retrieval/model cascading. [FactCheckmate](https://aclanthology.org/2025.findings-emnlp.663/) and [Internal States Reveal Hallucination Risk](https://aclanthology.org/2024.blackboxnlp-1.6/) also probe input states before answers.
- [Catching Rationalization in the Act](https://arxiv.org/abs/2603.17199) predicts hint-induced answer change immediately before chain-of-thought with question-disjoint splits. Its target is hint influence, not whether revision is normatively harmful.
- [KEEN](https://aclanthology.org/2024.emnlp-main.232/) predicts an entity’s average correctness over future questions, making Task A a new dialogue-level formulation rather than an unprecedented distribution-average risk target.
- [Semantic Entropy](https://www.nature.com/articles/s41586-024-07421-0) and [Semantic Entropy Probes](https://arxiv.org/abs/2406.15927) are strong continuation-distribution and prompt-state baselines, but uncertainty is not identical to falsity.
- [Good Arguments Against the People Pleasers](https://aclanthology.org/2026.acl-long.1126/) finds that sycophancy can evolve dynamically during chain-of-thought. A pre-generation score should therefore be framed as calibrated risk with irreducible uncertainty, not proof that the answer is already decided; a full study can compare pre-generation and mid-generation forecasts without contaminating the primary pre-response task.
- [Sycophancy Hides Linearly in Attention Heads](https://aclanthology.org/2026.eacl-long.324/) is mechanistically adjacent. A direct audit of its public code indicates full conversations including the target assistant answer are encoded and related question versions are randomly split; treat it as post-answer classification/steering evidence, not pre-response forecasting.

### Novelty conclusion

Do not title the paper “predicting hallucinations before generation” or claim a universal truth direction. The defensible contribution is a factorial, grouped-OOD study of whether a prior free-form answer creates **incremental vulnerability to a future evidence challenge**, and whether that pre-response increment enables a selective, cost-aware intervention.

## 1. Minimum viable 1–2 week study

Run the 60-family core and matched rewrite blocks in [the pilot protocol](PILOT_PROTOCOL.md). For Task A, capture features immediately after the prior answer and estimate mean error risk over a fixed future-challenge distribution. For Task B, append the challenge/evidence, capture again before decoding, and predict the soft risk across four continuations. Start with surface, semantic, prompt-logit, and residual features. Attention summaries are secondary; individual-head searches wait for a stable held-out effect.

Primary confirmatory comparison: Task B factors/question controls versus the same model plus Task-A risk, prior-answer features, and cross-turn representation change.

## 2. Higher-novelty mechanistic or causal version

Increase a stratified subset to 20–50 continuations; repeat on one held-out model family. Use content-preserving neutral/confident/hedged/deferential prior-answer rewrites. Test whether style changes post-challenge state and next-answer risk while content and next user message stay fixed. If a representation direction predicts on unseen questions/templates and mediates the randomized style effect, patch matched style-prefix residuals or selected head outputs at the challenge boundary. Freeze layer/head selection on validation data, then test behavior—not merely teacher-forced likelihood—on a locked split. Include random, layer-matched, shuffled-donor, and length/position-matched controls.

## 3. Falsifiable hypotheses

- **H1A:** Previous-response features predict Task-A susceptibility on unseen question families above difficulty, previous correctness, and response length, with positive out-of-fold Brier-skill improvement.
- **H1B:** Post-challenge states improve Task-B log loss over exact challenge/evidence factors, question difficulty, initial correctness, prompt text, and Task-A risk.
- **H1C:** Cross-turn residual deltas improve held-out calibration or log loss beyond either boundary state alone.
- **H1D:** At least one content-preserving stance rewrite changes harmful-drift probability versus neutral while its effect on beneficial correction is separately estimated.
- **H1E:** A risk-triggered verification policy improves error among answered at matched coverage relative to random and prompt-only triggers without materially lowering beneficial correction.

Null or reversed results are informative. If only question difficulty predicts, the susceptibility thesis fails. If an activation probe predicts but patching has no behavioral effect, the representation is correlational.

## 4. Unit of analysis

The sampling unit is a target continuation nested within a challenged prompt, prior-response prefix, question family, challenge-template family, and seed. Task A labels attach to a prior-response prefix as a weighted mean over its future challenge/continuation distribution. Task B labels attach to a unique challenged prompt as an empirical stochastic error probability. Statistical uncertainty is clustered at question family, never at row alone.

## 5. Independent and dependent variables

Independent variables:

- question stage/domain and controlled difficulty;
- initial-answer correctness;
- evidence profile and challenge template;
- rhetorical pressure;
- randomized prior-answer style in the causal block;
- generation seed;
- mitigation arm.

Predictors are grouped as surface stance, semantic consistency, prompt logits/entropy/answer margin, layerwise residual states, cross-turn deltas, attention summaries/head outputs, and counterfactual continuation statistics.

Dependent variables:

- target-answer correctness and soft factual-error risk;
- harmful drift, beneficial correction, justified persistence, stubbornness;
- evidence-assessment correctness;
- calibrated risk, false triggers, answered-case risk, latency, tokens, and compute;
- for causal work, behavioral risk difference and representation mediation.

## 6. Exact labels and data schema

Let Q be the question, A1 the previous model answer, C a challenge sampled from preregistered distribution D_C, and Y the next answer.

- Task A label: r_A(Q,A1) = expectation over C from D_C and Y from the frozen decoder of the indicator that Y is factually wrong.
- Task B label: r_B(Q,A1,C) = probability under the frozen decoder that Y is factually wrong.
- Secondary hard Task B label: correctness of the locked greedy answer.
- Challenge-induced excess risk: delta r = r_B(Q,A1,C) minus risk under a matched prefix with A1 removed or neutralized; define the reference before data collection.

The trial schema records question_family_id, stage, domain, initial answer/correctness, previous style, exact evidence fields, template family, evidence assessment, final answer/correctness, abstention, seed, split, prompt hash, model revision, and a feature timestamp fixed to pre_target_generation. It explicitly rejects target-response activations.

For open grounded answers, decompose claims and use deterministic span support where possible; otherwise require two independent evaluators plus a blinded human audit. Report judge disagreement and conclusions under each judge separately.

## 7. Confounders and controls

- Baseline knowledge/difficulty: include no-challenge/matched-challenge baselines, previous correctness, answer margin, and item effects.
- Question identity: group every normalized stem, entity, paraphrase, evidence variant, and rewrite.
- Exact user prompt: include prompt text/factors and evaluate held-out templates.
- Prior-response length/positions: match rewrites, record tokens/punctuation, and include length controls.
- Challenge type versus factual strength: cross rhetoric independently of validity, reliability, and diagnosticity.
- Decoder noise: fixed seeds/parameters and soft labels with uncertainty.
- Label noise: mechanical tasks first; blinded audit grounded QA.
- Representation dimensionality: PCA/scalers fit within training folds; matched-capacity baselines.
- Attention interpretation: describe only until intervention; control token span length and position.
- Multiple testing: small confirmatory hypothesis set plus FDR for exploratory layers/heads.

## 8. Recommended model

Qwen2.5-7B-Instruct in BF16. It is small enough for one modern 24 GB GPU and rich enough for multi-turn prompting. Pin revision. Use one Transformers-based reference path for activations; a throughput engine may reproduce behavior after chat-template parity tests.

## 9. Baselines

1. global and stage-conditioned base rates;
2. question/difficulty, initial correctness, and previous-answer margin;
3. response length and surface stance;
4. exact challenge/evidence fields and bag-of-words/embedding prompt model;
5. query-level internal-confidence analogue;
6. prompt-only residual probe;
7. previous-only and post-challenge-only probes;
8. cross-turn residual delta;
9. token entropy/answer margin;
10. semantic entropy or repeated-continuation disagreement;
11. always-on, random-at-matched-coverage, prompt-only, and oracle mitigation.

Report the incremental gain of every block; a high absolute AUROC with no gain over question/challenge controls is a negative result.

## 10. Grouped and OOD splits

Use 36/12/12 question-family train/validation/test with 12/4/4 families per stage. Group all variants of a question. Use nested leave-challenge-template-out evaluation and a locked question-plus-template test quarantine. Hold out an entire domain/stage as an OOD stress test. A later full study adds a model-family holdout. No scaling, PCA, feature selection, layer selection, calibration, or threshold tuning may see validation/test outcomes outside its permitted fold.

## 11. Metrics and statistical tests

Prediction: AUROC, AUPRC with prevalence, Brier score/skill, log loss, calibration slope/intercept, ECE with bin sensitivity, and risk-coverage curves. Use question-clustered bootstrap confidence intervals and paired out-of-fold loss differences. For hard outcomes use mixed-effects logistic regression with question and template random effects; if unstable, paired cluster bootstrap and transparent marginal contrasts. For soft labels use beta-binomial or binomial uncertainty and an N-continuation ablation.

Causality: average risk differences and odds ratios for randomized style contrasts, stage/evidence interactions, manipulation checks, equivalence bounds for preserved content, and exploratory mediation labeled as such. Intervention: paired accuracy/error reduction, beneficial-correction retention, false-trigger rate, coverage, added seconds/tokens/FLOPs, and cost curves.

## 12. Generations and compute

Combined one-week pilot: 23,040 core + 1,536 causal + 1,024 mitigation = **25,600 target generations**, roughly 2.05M output tokens at 80 tokens each. Budget 12–40 single-GPU hours on a 24 GB-class device, depending on context length and capture implementation. This is an estimate, not a measured result. Full study: raise approximately 1,000 stratified Task-B prompts from 4 to 20 continuations, adding 16,000 generations; add one replication model and head-intervention arms only after the pilot.

## 13. Expected artifacts

One week: frozen schemas/templates/splits, 25,600-row trial table, lightweight activation manifest, grouped baseline table, calibration/risk-coverage figures, causal rewrite contrasts, mitigation cost table, and error audit.

Full study: high-precision soft-risk subset, second-model replication, locked causal patching results, human-audited grounded labels, complete model/data cards, preregistration, and releasable aggregate artifacts.

## 14. Fastest failure diagnostic

Run the 3,072-generation 48-hour screen. Stop or redesign if harmful drift is below 10%, beneficial correction below 20%, parser error above 2%, cells are dominated by a few questions, or rewrite equivalence fails. After viability, fit question/evidence controls; if prior-response features and cross-turn states do not improve grouped validation log loss, abandon the forecasting contribution before collecting head-level activations.

## 15. PreferenceDrift-Bench contribution

It could supply audited question families, challenge templates, prior-answer trajectories, evaluator code, or an external-validation set. It cannot support Task A/B if capture occurs after the target answer, if exact evidence fields are missing, if both initial-correct and initial-wrong branches are absent, or if question/template groups cannot be reconstructed. No package was supplied, so none of those conditions is assumed.

# Direction 2 — mechanisms of conversational personality adaptation

## Chameleon reconstruction

[Chameleon LLMs](https://aclanthology.org/2025.emnlp-main.875/) defines personality operationally as a context-conditioned change in perceived Big Five traits—Extraversion, Agreeableness, Conscientiousness, Emotional Stability, and Imagination/Intellect—measured with IPIP-style assessment. It does not establish intrinsic human-like personality.

Protocol:

- 100 curated, deliberately strong user personas and 50 help/service scenarios;
- 20 total dialogue turns: 10 simulated-user and 10 chatbot turns;
- user always GPT-4o mini;
- seven chatbot models: GPT-4o, GPT-4o mini, Mistral Small 3 24B Instruct 2501, Phi-4 14B, Llama 3.1 8B Instruct, Qwen2.5 7B Instruct, and Gemma 2 2B Instruct;
- 1,000 nominal simulations per chatbot model, temperature .7, chatbot maximum 100 tokens;
- IPIP-50 before and after dialogue, ten items per trait, one item per separate call, five-point Likert, reverse-keyed where required, trait scores 10–50;
- trait shift equals post-context score minus model baseline score.

The main analysis correlates the simulated user’s initial trait with the chatbot’s trait shift in 5×5 matrices. The paper reports generally positive same-trait relationships, weaker Emotional Stability adaptation, and non-monotonic model-size effects. Those are published findings, not results reproduced here.

Prediction uses five linear regressions, one per target trait. The paper says 31 features and 7,000 observations, while Appendix Table 9 enumerates 25 conceptual numeric features: five user traits, five chatbot baselines, five user-minus-chatbot differences, sentiment, model size, six scenario ratings, and two mean character lengths. Reported R² ranges .25–.64. Because difference variables are linear combinations of included scores, coefficients should not be interpreted causally.

Amplify/resist prompting uses GPT-4o mini with 500 simulations per condition. Explicit mirroring increases trait correlations; “do not change/imitate” does not significantly reduce them. Example outputs visibly mix punctuation, tone, behavior, and interests, so the result is not a clean Big Five mechanism.

Temporal analysis uses 100 Mistral Small 3 conversations, 60 total turns, and IPIP assessment after each chatbot response, yielding baseline plus 30 measurements. The paper reports early movement in several traits. WildChat analysis filters English conversations, truncates to 20 turns, and reports 600 sampled chats; GPT-4o mini replays the assistant, infers user traits, and receives only a post-test against a shared baseline. It supports ecological association, not causal identification.

Measurement limitations:

- IPIP response consistency and factor validity in LLMs are contested;
- post-test scores include dialogue context and may primarily measure perceived persona enactment;
- the same/similar model family helps simulate, replay, and assess;
- extreme personas, English prompts, synthetic users, and service scenarios limit generality;
- lexical/punctuation imitation can drive perceived traits;
- one model-level baseline ignores run-level questionnaire variance;
- many correlations require multiplicity control;
- model size is confounded with family/training.

Artifact audit of the [official repository](https://github.com/xingdom/chameleon-llms) found code, personas/scenarios, outputs, and analysis scripts, but also count discrepancies, incomplete model runs, row-level random splits, preprocessing before splitting, undocumented score anomalies, no leave-persona/scenario-out tests, and serious temporal/WildChat reproducibility defects. These findings should be independently rechecked against a pinned commit before citing exact line-level bugs. Most importantly, Chameleon’s “interpretability” analysis is output-feature regression. **Chameleon does not identify hidden-state layers, neurons, attention heads, sparse features, or causal circuits.**

## Novelty boundary

Simply discovering a Big Five direction, “personality layer,” head, or neuron is not novel after:

- [Personality Alignment of LLMs](https://arxiv.org/abs/2408.11779), which probes and edits personality-related attention heads;
- [Neuron-based Personality Trait Induction](https://arxiv.org/abs/2410.12327), which locates and manipulates FFN neurons;
- [Activation-Space Personality Steering](https://aclanthology.org/2026.eacl-long.300/), which learns low-rank Big Five subspaces and trait-specific layers;
- [PERSONA](https://arxiv.org/abs/2602.15669), which dynamically composes Big Five activation vectors across turns;
- [Linear Personality Probing and Steering](https://arxiv.org/abs/2512.17639), which fits continuous IPIP directions;
- [DPN-LE](https://aclanthology.org/2026.findings-acl.1528/), which edits sparse Big Five neuron sets;
- [A Mechanistic Interpretability Perspective on Personality](https://www.sciencedirect.com/science/article/pii/S0306457326003535), which reports static Big Five circuits.

The defensible gap is whether **unprompted user-induced** trait shift in matched ordinary dialogue uses the same representations as statically assigned traits, when it emerges, whether it mediates behavior beyond lexical imitation, and whether harmful mirroring can be selectively suppressed.

## 1. Minimum viable 1–2 week study

Use 20 matched user personas: two independent realizations for each of ten Big Five poles; 10 scenarios; two seeds; 400 dialogues, each with ten assistant turns. Freeze user scripts so only the assistant model varies. Collect ten independently seeded, randomized IPIP-50 model baselines (not one reused deterministic baseline), one post-dialogue IPIP-50 per dialogue, plus open-ended trait judgments from a distinct evaluator and lexical accommodation measures.

This requires 4,000 dialogue generations, 20,000 post-IPIP item responses, and 500 baseline-item responses. Add turn-resolved IPIP after assistant turns 1, 5, and 10 only for a balanced 60-dialogue subset: 9,000 more item responses. Exact planned chatbot-model total: **33,500 short generations**, excluding the frozen user-script authoring and independent evaluator calls. First test whether trait-specific shift survives leave-persona-out and leave-scenario-out evaluation after controlling lexical style.

## 2. Higher-novelty mechanistic or causal version

Learn static high/low trait directions from an independent dataset, never from evaluation dialogues. Create proposition-matched user-prefix pairs whose trait realization differs while facts, intent, scenario, length, and dialogue act remain fixed. Capture assistant states after each user/assistant turn. Compare static and induced subspaces by cosine similarity, CCA/subspace angles, and cross-decoding. Patch high-pole versus low-pole matched user-prefix residuals by turn/layer, then refine to heads/MLPs/SAE features. Test prompt resist, activation suppression, combined, amplification, random-vector, and sham interventions on held-out personas/scenarios. Validate behavior, not questionnaire scores alone.

Optional personality–factuality extension: cross one target-trait manipulation, valid/invalid evidence, neutral/high pressure, and initial correct/wrong while scoring personality and factuality separately. Retain only if manipulation checks show trait variation without changing evidence propositions or factual content and every cell is adequately powered. Otherwise drop it.

## 3. Falsifiable hypotheses

- **H2A:** User target-trait pole predicts the matching post-minus-pre IPIP score on held-out personas and scenarios after controlling length, punctuation, sentiment, and lexical alignment.
- **H2B:** A turn-by-layer representation trained on independent trait data predicts later target-trait shift before the final dialogue turn; non-target traits show materially smaller effects.
- **H2C:** Matched-prefix patching changes target-trait behavior/IPIP score in the donor direction on held-out dialogues, while sham/random patches do not.
- **H2D:** Prompt “resist” and activation suppression differ: activation intervention reduces target-trait mirroring more while preserving lexical accommodation, helpfulness, coherence, and task success.
- **H2E:** Static assigned-personality and user-induced adaptation directions are not assumed identical; either preregister a minimum subspace overlap or treat separability as a competing hypothesis.

## 4. Unit of analysis

A questionnaire item is a measurement nested in trait, assessment occasion, dialogue, persona realization, scenario, and seed. The causal unit is a matched dialogue prefix at a specified assistant turn, patched at a specified layer/component. Cluster at persona realization and scenario; do not treat 50 questionnaire items as 50 independent dialogues.

## 5. Independent and dependent variables

Independent: user target trait/pole, matched realization, scenario, turn, model, resist prompt, activation intervention, component/layer, and lexical-control condition.

Dependent: target and non-target IPIP shifts; open-ended perceived-trait rating; trait-specific behavioral score; lexical/punctuation accommodation; representation score; task success, factuality, fluency, helpfulness, coherence, refusal/length; MMLU/ARC or an equivalent small capability suite.

Keep five constructs separate: lexical imitation, perceived Big Five shift, adaptation susceptibility, factual belief state, and evidence weighting.

## 6. Exact labels and schema

Record dialogue_id, persona_family_id, persona_realization_id, target_trait, target_pole, scenario_family_id, turn_index, immutable messages/hash, model revision, pre/post IPIP item responses and reverse keys, five trait scores/shifts, open-ended rating, lexical features, intervention specification, capture boundary, component coordinates, task-quality measures, split, and seed.

The primary personality label is target-trait post-context minus independently measured pre-context IPIP score. Non-target shifts are negative controls. “Adapted” is not a generic binary label; if needed, define it by a preregistered minimally important target-trait change and report the continuous score.

## 7. Confounders and controls

Control questionnaire order, acquiescence/reverse-key inconsistency, rater-model identity, baseline variance, context-length/recency, extreme-persona content, semantic proposition changes, length/punctuation/sentiment, scenario power/stakes, model-role confusion, and repeated measures. Include neutral persona, shuffled history, punctuation-normalized, length-matched, synonym/paraphrase, explicit assigned-trait, sham patch, random component, and non-target-trait controls. Correct multiplicity across trait×layer/component tests.

## 8. Recommended model

Qwen2.5-7B-Instruct provides direct behavioral comparability with Chameleon and full internal access. Confirm the behavioral effect before activation capture. For cross-model validation, choose a different family—not merely another Qwen size.

## 9. Baselines

Chameleon’s surface/model/scenario regression; lexical n-grams and punctuation; sentiment and length; prompt-assigned trait classifier; static independent trait direction; random layer/head/neuron directions; prompt amplify/resist; shuffled user histories; neutral matched dialogue; always suppress versus no intervention.

## 10. Grouped and OOD splits

Leave persona families out, so near-duplicate labels or tropes cannot cross splits. Independently leave scenario families out. Keep all paraphrases, turns, interventions, and seeds of a dialogue family together. Report trait-pole-balanced cross-validation and a locked persona×scenario Cartesian holdout. Later test a second model family and less exaggerated/naturalistic users.

## 11. Metrics and statistical tests

Continuous trait shift with hierarchical linear models; target-minus-average-nontarget specificity; ICC/test–retest reliability; reverse-key consistency; convergent validity across IPIP, open-ended raters, and behavioral rubrics; cross-decoding AUROC/R² for representations; paired causal effect with question/dialogue-clustered bootstrap; intervention selectivity as target-shift reduction minus non-target/quality degradation. Apply Holm or Benjamini–Hochberg correction. Report effect sizes and CIs, not only correlation significance.

## 12. Generations and compute

Behavioral MVP is approximately 33k short generations, dominated by IPIP calls, plus 4,000 dialogue responses. Batched local scoring is feasible in one week on a single 24 GB GPU. The mechanistic version should first record final-token/segment-pooled residuals for 400 dialogues; patch only validation-selected turns/layers on roughly 100 held-out matched prefixes. Full exhaustive head patching across every turn is unnecessary and likely wasteful.

## 13. Expected artifacts

One week: a Chameleon reproduction audit; matched persona/scenario scripts; reliability/lexical-control table; leave-persona/scenario-out trait-shift results; lightweight turn×layer maps.

Full study: independent trait-direction training set, proposition-equivalence audit, causal patching/ablation results, prompt-versus-activation intervention comparison, quality/capability safeguards, second-model replication, and human/open-ended validation.

## 14. Fastest failure diagnostic

On 20 matched dialogues, remove punctuation/style markers and compare IPIP plus an independent open-ended rater. If the target-trait effect vanishes, reverse-key reliability is poor, or neutral paraphrases produce shifts as large as target personas, stop mechanistic localization: the outcome lacks construct validity. Also stop if leave-persona/scenario-out prediction collapses while row-random performance looks strong.

## 15. PreferenceDrift-Bench contribution

The package could contribute conversational templates, style manipulations, or quality/factuality safeguards. It cannot supply Big Five labels unless it includes validated IPIP-style pre/post measurement and independently controlled trait realizations. Preference drift is not personality drift by definition. Direction 2 remains scientifically coherent without it.

# Direction 3 — evidence-sensitive answer revision

## Operational problem and prior-work boundary

The core problem is not “does the answer flip?” It is whether the model gives the correct weight to evidence after independently appraising validity, relevance, diagnostic strength, source reliability, relation to the current answer, rhetoric, repetition, and dependence.

The four minimum outcomes are:

| Initial state | Evidence | Final correct | Outcome |
|---|---|---|---|
| Correct | invalid, decisive-looking, contradicts gold | yes | justified persistence |
| Correct | invalid, decisive-looking, contradicts gold | no | harmful drift |
| Wrong | valid, decisive, supports gold | yes | beneficial correction |
| Wrong | valid, decisive, supports gold | no | stubbornness |

Supporting, irrelevant, insufficient, ambiguous, and conflicting evidence require separate labels; they do not belong in the headline four-cell denominator by convenience.

Several broad claims are already occupied:

- [SycoBench-600](https://aclanthology.org/2026.findings-acl.1759/) defines Update, WrongFlip, and Selectivity = Update − WrongFlip over balanced correct/wrong suggestions. The proposed Update Selectivity difference is useful but not new.
- [Teaching Models to Balance Resisting and Accepting Persuasion](https://aclanthology.org/2025.naacl-long.412/) trains on balanced correction/resistance dialogue trees. This project cannot claim the first balanced training objective.
- [Belief-R](https://arxiv.org/abs/2406.19764) evaluates Belief Update, Belief Maintain, and their balanced mean; its psychologically motivated added-premise judgments are not an externally verified evidence model.
- [BASIL](https://arxiv.org/abs/2508.16846) compares belief shifts with a Bayesian-consistent posterior and proposes calibration/training. Its normative target uses model-elicited priors and likelihoods, whereas this design starts with externally known likelihoods/provenance.
- [Resist and Update](https://arxiv.org/abs/2607.12985) is the most direct collision: it uses exact Bayesian witnesses, makes the same disagreement licensed evidence or forbidden pressure through source reliability, studies Qwen2.5-3B/7B and other small models, causally localizes late report coordinates, and proposes a hidden-state clamp. It leaves no public code/data link in the paper, so the result requires reproduction, but it occupies “Bayesian reliability×pressure plus activation intervention” almost verbatim.
- [Fundamental Problems With Model Editing](https://arxiv.org/abs/2406.19354) uses exact Categorical–Dirichlet posterior predictions for rational weight editing, establishing a strong precedent for magnitude-sensitive metrics.
- [Truth or Dare](https://aclanthology.org/2026.trustnlp-main.39/) manipulates false-evidence rhetoric, quantity, and semantic similarity, but lacks valid corrective branches and treats repeated paraphrases without explicit shared provenance.
- [DeReLab](https://arxiv.org/abs/2608.30413), accepted at EMNLP 2026 immediately before this review cutoff, already provides mechanically resolved multi-turn defeasible graphs, effect appraisal, irrelevant updates, source-priority conflicts, and a large appraisal-versus-answer dissociation. Mechanically verified revision and “assess the effect first” are therefore not novel by themselves.
- [Accounting for Sycophancy in Uncertainty Estimation](https://aclanthology.org/2025.findings-naacl.438/) already crosses suggestion correctness with stated user confidence and calibrates correctness; confidence wording is not evidence reliability.

Direction 3 alone now has **very high novelty risk**. Its defensible role is primarily to create controlled labels for Direction 1. Any secondary D3 claim must go beyond Resist and Update and DeReLab through correlated/repeated/irrelevant/ambiguous multi-evidence, nonbinary posterior magnitude, explicit appraisal-versus-policy causal decomposition, and transfer from Bayesian tasks to mechanical and fixed-passage factuality. Explicit appraisal is a measurement device, not a novelty claim, and its prompt-order sensitivity must be tested.

## 1. Minimum viable 1–2 week study

Run the 60-family/8-profile behavioral core. Stage 1 uses transparent Bayesian tasks with exact priors, likelihood ratios, source dependence, and posterior answers. Stage 2 uses arithmetic, logic, code, and table tasks with deterministic validators. Stage 3 uses fixed passages with frozen provenance and answer spans. Elicit a compact structured evidence assessment before the final answer in the main condition, with a counterbalanced answer-first condition on a diagnostic subset because DeReLab shows that question order can change appraisal accuracy. Measure four headline outcomes, other evidence cells, appraisal accuracy, update direction/magnitude, and failure decomposition.

## 2. Higher-novelty mechanistic or causal version

At the post-challenge/pre-answer boundary, probe evidence-appraisal variables separately from update action. Perform an oracle-appraisal intervention: supply the correct structured evidence fields while preserving the evidence text, then compare final updating. If final correctness improves, appraisal is upstream; residual failures identify update policy. Conversely, hold appraisal text fixed and alter an activation direction only after validating it on held-out questions. Use Bayesian tasks to test monotonic, magnitude-sensitive behavior across multiple correlated and independent evidence objects. Compare explicitly with Resist and Update’s reported late report coordinates; do not relabel their intervention as new.

A later training study may optimize appraisal and update policy separately, but cannot claim first balanced accept/resist training. Compare evidence-verification prompting, retrieval/checker gating, balanced SFT/DPO, and activation intervention under equal compute.

## 3. Falsifiable hypotheses

- **H3A:** Validity, relevance, diagnosticity, reliability, and independence have separable effects in the normatively correct direction after controlling rhetoric.
- **H3B:** Repeating non-independent evidence changes the model more than the normative posterior permits; explicitly marking shared provenance reduces that over-update.
- **H3C:** Evidence-assessment accuracy predicts final update quality, but a non-zero set of update-policy failures remains after correct appraisal.
- **H3D:** Oracle appraisal improves harmful-drift and stubbornness rates relative to free appraisal, with a larger effect where appraisal is initially wrong.
- **H3E:** A selective gate improves normative update regret and answered-case correctness over always-accept, never-change, random, and always-verify policies at matched cost.

## 4. Unit of analysis

A target continuation nested within evidence profile, challenged prompt, initial-answer branch, question family, stage/domain, template, and seed. Bayesian probability estimates are additional outcomes within the same unit. Dependence manipulations cluster repeated pieces by evidence provenance, not by text string.

## 5. Independent and dependent variables

Independent: initial correctness; evidence validity, relevance, diagnostic strength, source reliability, relation to gold, rhetoric, repetition count, dependence group; stage/domain; template; intervention; seed.

Dependent: structured appraisal fields; final correctness/abstention; answer flip and destination; four headline outcomes; posterior probability; normative direction and magnitude error; Update Selectivity; appraisal/policy failure; latency/tokens/compute.

## 6. Exact labels and data schema

Evidence record:

- evidence_id and immutable text/hash;
- validity: valid, invalid, ambiguous, not applicable;
- relevance: relevant, partial, irrelevant;
- diagnostic_strength in [0,1] plus the exact likelihood ratio in Bayesian tasks;
- source_reliability in [0,1] with stated provenance;
- relation_to_gold: supports, contradicts, neutral, mixed;
- rhetorical_pressure: neutral/high, independently randomized;
- repetition_count;
- independence_group;
- generator/verifier version and provenance.

Trial record additionally includes gold/distractor, prior and final answer/probability, initial/final correctness, evidence assessment, abstention, outcome, model revision, prompt hash, split, and seed. Ambiguous/insufficient cells receive their own expected-policy labels rather than being squeezed into persist/flip.

## 7. Confounders and controls

Separate source reputation wording from calibrated source reliability; confidence from diagnosticity; repetition from independence; validity from agreement with the initial answer; relevance from length; rhetoric from content; initial correctness from model confidence. Match token counts and syntax where possible. Use gold-generating programs, source hashes, independent item verification, shuffled-source controls, duplicate-versus-independent evidence, and counterbalanced support/contradict directions. Audit whether the “wrong initial answer” is genuinely produced by the model or externally inserted; analyze these separately.

## 8. Recommended model

Qwen2.5-7B-Instruct in BF16, with a frozen prompt contract and deterministic evaluators. Stage 3 should use only passages included in context so world-knowledge changes do not corrupt labels.

## 9. Baselines

Always maintain, always flip, follow latest message, follow most confident wording, majority over repetitions, source-reliability heuristic, exact Bayesian updater, prompt evidence checklist, self-consistency, retrieval/deterministic checker, SycoBench-style selectivity, BASIL-style internal-coherence calibration, and random/always-on/oracle gates.

## 10. Grouped and OOD splits

Group by underlying generative program/question family and challenge template. Keep support/contradict counterfactuals, paraphrases, repetitions, and initial-state branches together. Hold out one stage/domain and one template family. For Bayesian generators, hold out parameter ranges and causal-graph structures, not merely random seeds.

## 11. Metrics and statistical tests

- Conditional beneficial-correction and harmful-drift rates with question-clustered intervals.
- Update Selectivity, explicitly credited as overlapping SycoBench.
- Balanced four-outcome macro accuracy and full confusion matrix.
- Per-field appraisal accuracy/F1 and joint exact match.
- Appraisal-policy decomposition.
- Bayesian posterior Brier/log loss, signed direction error, magnitude error, and update regret: final Brier to normative posterior minus prior Brier.
- Risk/coverage and utility/cost for gates.

Use factorial mixed-effects models and question-clustered bootstrap contrasts; analyze ordinal reliability/strength monotonically; test repetition×independence and validity×rhetoric interactions. Preregister a small family of primary contrasts and control exploratory multiplicity.

## 12. Generations and compute

Behavioral core is 23,040 target generations and shares labels with Direction 1. Without activations this is a modest 7B inference study. Oracle-appraisal and two mitigation arms add roughly 1,000–3,000 short generations depending on the locked subset. Bayesian posterior generation/evaluation is CPU-cheap; model decoding dominates.

## 13. Expected artifacts

One week: three-stage item generator, eight-profile evidence set, validators, 23,040-row behavior table, ontology/confusion matrix, appraisal-policy audit, normative-update plots, and intervention pilot.

Full study: larger exact-posterior suite with dependence graphs, external grounded-QA audit, second-model replication, oracle-appraisal causal analysis, calibrated gate, and possibly a balanced training comparison.

## 14. Fastest failure diagnostic

Run 8 Bayesian and 8 mechanical families with neutral rhetoric. Check whether the model’s structured appraisal distinguishes valid from invalid evidence above 80% and whether both harmful drift and beneficial correction occur. If labels cannot be made mechanically unambiguous, if outputs ignore the required schema, or if “effects” vanish when rhetoric is matched, stop before building a benchmark.

## 15. PreferenceDrift-Bench contribution

It may provide candidate revision traces and realistic prompts, but only externally verifiable rows can enter the main study. If its factors are entangled, reserve it for external validity. It cannot establish normative evidence weighting without provenance, likelihood/diagnosticity, independence, initial-state branches, and pre-answer appraisal.

# Combination decision

## Directions 1 and 3: combine narrowly

They combine naturally because Direction 3 supplies controlled challenge/evidence contexts and interpretable outcomes, while Direction 1 asks whether those outcomes can be forecast before generation. The same factorial dataset supports both without merging labels.

Required identification checks:

1. Define Task A, Task B, appraisal, and final correctness separately.
2. Randomize or mechanically generate evidence attributes independently where logically possible.
3. Capture all predictors before target decoding.
4. Keep question content, previous answer, evidence text, and prompt template immutable within matched branches.
5. Use repeated continuations for risk rather than retrofitting target activations.
6. Maintain adequate samples in each initial-correctness×validity×pressure cell.
7. Test incremental prediction beyond exact factors and difficulty.
8. Treat causal style rewrites and evidence manipulations as separate estimands.

Recommended paper-level framing:

> **Forecasting Evidence-Induced Factual Failure Before the Next Answer**
>
> We construct mechanically and source-grounded dialogue branches that separate evidence appraisal from update policy, estimate pre-challenge susceptibility and post-challenge risk without target-response activations, test causal prior-answer stance with matched rewrites, and evaluate a calibrated verification gate.

This is one coherent prediction-and-intervention story. Avoid advertising a new benchmark unless the item set later demonstrates breadth, reliability, and external use beyond the paper.

## Direction 2: keep separate

Personality–factuality is not needed for the recommended paper. It can become a later factorial study only if:

- personality manipulation changes IPIP/open-ended target-trait measures;
- lexical style and propositions are matched;
- evidence validity, rhetoric, and initial correctness vary independently;
- factuality and evidence appraisal use their own labels;
- enough observations exist in every trait×evidence×initial-state cell;
- mediation uses pre-outcome measurements and matched prefixes.

Until then, adding personality mainly creates construct confusion and a multiplicative sample burden.

# Final action package

## 1. Single experiment for the next 48 hours

Run the **3,072-generation matched behavioral viability screen** on Qwen2.5-7B-Instruct: 24 question families × 2 initial states × 2 decisive evidence conditions × 4 content-preserving prior-answer styles × 2 rhetoric levels × 1 fixed template × 4 seeds. Collect structured evidence appraisal before the final answer. The exact protocol and gates are in [PILOT_PROTOCOL.md](PILOT_PROTOCOL.md).

The immediate decision is whether harmful drift and beneficial correction are both observable, mechanically labelable, and not driven by parser/question artifacts; the secondary decision is whether stance deserves a causal role. Do not start a head search in these 48 hours.

## 2. Seven-day schedule

1. **Day 1:** freeze constructs, gold items, schemas, rewrite-equivalence rubric, and prompt hashes.
2. **Day 2:** run/review the 3,072-generation screen and apply go/no-go gates.
3. **Day 3:** finish 60 families, three template families, grouped splits, and leakage audit.
4. **Day 4:** run 23,040 core generations with lightweight pre-response capture and manifests.
5. **Day 5:** fit grouped, calibrated nested baselines; estimate Task A/Task B labels and uncertainty.
6. **Day 6:** run 1,536 causal and 1,024 mitigation generations; analyze appraisal versus policy.
7. **Day 7:** execute the locked test analysis once; create tables, cost report, failure audit, and continue/pivot/stop memo.

## 3. Exact pilot matrix and generation count

| Block | Matrix | Count |
|---|---|---:|
| Core | 60 questions × 2 initial states × 8 evidence profiles × 2 pressure levels × 3 template families × 4 seeds × 1 style | 23,040 |
| Causal rewrites | 24 questions × 2 initial states × 2 evidence profiles × 1 pressure × 1 template × 4 seeds × 4 styles | 1,536 |
| Mitigation | 128 locked contexts × 2 arms × 4 seeds | 1,024 |
| **Total** | — | **25,600** |

## 4. Files and modules to create

The repository already supplies the design-level versions of:

- configs/pilot.toml;
- schemas/item.schema.json, evidence.schema.json, trial.schema.json, manifest.schema.json;
- data/templates/evidence_profiles.json;
- model-adapter, branching, metrics, grouped-split, evaluator, probe-contract, gate, and manifest modules;
- count/materialization/validation scripts and unit tests;
- research, literature, architecture, pilot, and PreferenceDrift intake documents.

Before running a model, implement concrete transformers_adapter.py, prompt_renderer.py, Bayesian/mechanical item generators and validators, activation_hooks.py, feature_extraction.py, probe_training.py, analysis.py, and blinded_rewrite_audit.py. Add an immutable environment lock and pin every model/dataset revision.

## 5. Do not do yet

- Do not claim the first pre-generation factuality detector, pre-onset yield predictor, selective-updating metric, balanced accept/resist training method, Big Five direction, personality layer, or personality circuit.
- Do not combine all three directions into one paper.
- Do not use target next-response activations in a pre-response predictor.
- Do not randomly split rows, paraphrases, pressure variants, personas, or scenarios.
- Do not run exhaustive head/neuron searches before a grouped behavioral effect and calibrated incremental predictor exist.
- Do not equate attention correlation, probe accuracy, or teacher-forced likelihood change with a causal behavioral mechanism.
- Do not use LLM judges as the sole factuality label where mechanical verification is possible.
- Do not conflate confidence wording with evidence strength or source reliability.
- Do not launch large-scale training, retrieval infrastructure, multiple model families, or full WildChat work in week one.
- Do not import PreferenceDrift-Bench until its license, provenance, schema, leakage, and labels pass the intake audit.

## 6. Three questions for the professor

1. Is the intended contribution primarily a causal science result about prior-answer/evidence processing, or a deployable risk gate? That choice determines whether continuation budget goes to matched interventions or broader calibration/OOD testing.
2. May we frame Directions 1 and 3 as one study—forecasting evidence-induced factual failure—with the evidence benchmark serving as controlled substrate rather than a separate benchmark claim?
3. Was the PreferenceDrift-Bench package omitted from the attachment, and if so can we obtain a versioned copy with license, provenance, raw labels, prompts, and model-generation settings before deciding whether to reuse it?

## 7. Meeting-document paragraph

I think the strongest next step is to combine the forecasting question with a tightly controlled answer-revision setup, while keeping the personality project separate. The broad idea of detecting an error before generation is no longer enough on its own—recent work already does that—so the useful gap is whether a model’s previous answer creates additional vulnerability to a specific evidence challenge, after we control for what the question is, whether the first answer was correct, and exactly what the user says next. I would start with a small matched experiment that includes both bad changes and good corrections, asks the model to assess the evidence before answering, and varies only the style of the previous answer. If that effect is real and survives grouped splits, we can then test internal representations and use the risk estimate to trigger verification; if it is not, we will know within two days and can pivot without having built a large benchmark.
