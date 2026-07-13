# Comparative Representation Protocol, Version 1.0

Status: Accepted methodology for comparative representation evaluation  
Version: 1.0  
Protocol identifier: CRP-1.0  
Scope: comparative, blinded, preregistered testing of representational vocabularies  
Lock rule: frozen before evaluator exposure; any substantive change creates a new protocol version.

## Purpose and Scope

The Comparative Representation Protocol v1.0 compares representational vocabularies under blinded, preregistered conditions. It is a methodology and governance artifact. It does not modify Foundation v1.0, FAR primitives, FARA primitives, FARO, FARE, FARM, canonical definitions, axioms, lemmas, propositions, theorems, accepted proof objects, accepted mathematical dependency metadata, mechanization behavior, parser behavior, CLI behavior, or accepted doctrine.

Registered research question:

> Among the tested representational vocabularies, does the target vocabulary preserve the fixed systems while imposing more reproducible and economically useful structural constraints, and do its primitive categories survive local ablation without loss or equivalent reconstruction?

This protocol governs future claims that a tested vocabulary is existentially sufficient, reproducibly sufficient, structurally more reproducible than weaker baselines, more economical in normalized representation cost, locally necessary under symmetrical primitive ablation, matched by weaker vocabularies, or Pareto-dominated by weaker vocabularies.

## Binding Non-Claims

Version 1.0 does not establish universality, global minimality, uniqueness, metaphysical necessity, adequacy for all reasoning, or superiority over all possible vocabularies. Version 1.0 results may not be silently pooled with later versions.

## Relationship to Preliminary External Validation

External validation remains useful for preliminary case description, scoped FAR/FARA mapping, preliminary preservation analysis, candidate-counterexample identification, and exploratory evidence collection. Successful FAR/FARA mapping is not comparative evidence. Comparative Representation Protocol v1.0 governs future claims about distinctiveness, reproducibility, local necessity, relative economy, and stronger comparative interpretation. Legacy external-validation reports retain their original evidence status and must not be retroactively presented as Version 1.0 experiments.

## Registered Hypotheses

- `H_{S,exists}` — existential sufficiency: at least one mapping for vocabulary `V` preserves every required preservation dimension with `Pass`, triggers no failure criterion, and leaves no required property `Unknown`.
- `H_{S,rep}` — reproducible sufficiency: all three primary mappings for vocabulary `V` meet the existential sufficiency condition in this experiment.
- `H_{C,G}` — comparative structural reproducibility: the target vocabulary has no worse comparable preservation, no required `Unknown`-blocked comparison, higher structural agreement `G_s` than both baselines, and is not Pareto-dominated on representation cost.
- `H_{C,R}` — comparative representation economy: the target vocabulary has no worse comparable preservation, no required `Unknown`-blocked comparison, Pareto-dominates both baselines on representation cost `R`, has at least one material cost advantage over each baseline, and has no lower `G_s`.
- Local necessity through symmetrical primitive ablation: a primitive is locally necessary only to the registered degree supported by the ablation rules in this protocol.

`H_S` may be used only as an umbrella reference to `H_{S,exists}` and `H_{S,rep}`; it is not an undifferentiated hypothesis.

## Experiment 1 Registration

Comparative Representation Experiment 1: Reflective Discrete Rule-Transition System (`CRE-001`) is registered under protocol `CRP-1.0`. Its conclusions apply directly only to systems characterized by discrete states, explicit propositions, explicit rules, explicit transitions, self-modification, historical dependency preservation, and explicit termination conditions.

## Candidate Vocabularies

The registered candidate vocabularies are:

1. objects, relations, and transformations;
2. states, transitions, and labels;
3. representation, representational structure, interpretation, investigation, and calculus.

Evaluator-facing materials must anonymize and randomize vocabulary labels. The vocabulary identities, randomization record, and assignment record must be preserved outside evaluator-facing packets until unblinding.

## Evaluator Design

Each vocabulary receives three independent evaluators, for nine primary mappings total. Each evaluator receives one vocabulary. Evaluators must have fixed eligibility criteria, formal-specification competence, relevant methodological familiarity, independence from vocabulary and protocol development, information isolation, and standardized unrelated calibration. Exclusion is permitted only for preregistered procedural violations.

## Baseline Symmetry

All vocabularies receive identical scenario, success and failure criteria, derived-machinery permissions, instructions, output schema, time or token budget, canonicalization, scoring, equivalence, adjudication, and interpretation rules.

## Permitted Derived Machinery

Every derived construct must record declaration, formal role, supplied category under which it is introduced, preservation requirement served, necessity for the mapping, and provenance. Derived machinery may not alter the scenario or introduce unstated domain rules.

## Canonical Intermediate Representation

The fixed CIR schema contains: primitive categories used; derived construct declarations; state variables; relation declarations; transition schemas; admissibility conditions; historical constraints; status-transition rules; termination conditions; preservation vector; and observable outputs.

Every CIR component must record component identifier, CIR section, component type, formal content, origin, supporting source, preservation role, and canonicalization status. The origin must be exactly one of `scenario`, `vocabulary`, or `derived`.

## Canonicalization Algorithm

Canonicalization proceeds in this order: remove lexical and presentational variation; extract semantic components; separate compound constructs; merge redundant subdivisions; test operational and commitment equivalence; remove strict redundancy; populate the CIR; compute metrics only from the final CIR.

## Equivalence

Operational equivalence means constructs permit the same state transitions, updates, admissibility effects, termination effects, and observable outputs under the registered scenario. Commitment equivalence means constructs introduce no materially different entity distinctions, state variables, relation types, admissibility restrictions, historical information, hidden state, modal distinctions, semantic distinctions, or ontological commitments. Full canonical equivalence holds only when operational and commitment equivalence both hold. Constructs may merge only under full canonical equivalence.

## Preservation Vector

`P = (p_s, p_m, p_o, p_d, p_i, p_h)` records structural, semantic, operational, dependency, information, and historical preservation. Allowed values are `Pass`, `Partial`, `Fail`, and `Unknown`. The partial order is `Pass > Partial > Fail`; `Unknown` is epistemically incomparable with non-`Unknown` values. A mapping supports existential sufficiency only when every required dimension is `Pass`, no failure criterion is triggered, and no required property remains `Unknown`.

## Sufficiency and Reproducibility

For vocabulary `V`, `S_V = successful mappings / 3`. Interpret `0/3` as sufficiency not demonstrated; `1/3` as existential sufficiency demonstrated but highly fragile; `2/3` as existential and majority mapping-level sufficiency demonstrated; and `3/3` as reproducible sufficiency demonstrated for the experiment. Keep `S_V`, conservative vocabulary-level preservation profile `P_V`, and structural agreement `G_s` separate.

## Vocabulary and Representation Cost

Report vocabulary cost separately as `V_V = (median A_used, median A_required)`. Report representation cost as `R_V = (median D, median O, median L)`, where `D` is normalized indispensable derived construct types, `O` is normalized transition or update schemas, and `L` is normalized atomic semantic clauses. Vocabulary and representation cost must not be combined into one weighted score.

## Clause Segmentation

One atomic clause is exactly one typed declaration, condition, permitted transition, prohibited transition, state update, status update, dependency requirement, historical constraint, termination condition, or observable-output requirement. Independent conjunctions are split. Conditional updates count as condition plus update unless indivisible in the source formalism. Alternatives are separate clauses for each permitted alternative. Biconditionals split into two directed conditions unless the source gives an indivisible equivalence rule. Quantification is part of the clause it governs unless it introduces distinct typed declarations. Semantic duplicates are counted once after canonicalization. Compound records split by typed field when fields carry independent semantic force. Lexical variation never creates an additional clause. Clause records must be machine-readable or table-convertible and must include identifiers and clause types.

## Agreement

`G_v` is verdict agreement. `G_s` is structural agreement computed from the three independently canonicalized mappings for each vocabulary. Evaluator CIRs must not be replaced with a consensus CIR for agreement or primary complexity measurement.

## Symmetrical Ablation

Every primitive in every vocabulary is ablated. Each primitive receives three independent ablation mappings. Classify each ablation as preservation loss, equivalent reconstruction, material representation-cost increase, tradeoff, no qualifying effect, or `Unknown`. A primitive is replicated locally necessary at `3/3`, provisionally locally necessary at `2/3`, inconclusive at `1/3`, and not shown locally necessary at `0/3`. `Unknown` does not count as successful removal or survival.

## Material Cost Increase

Use Pareto comparison on `R = (D, O, L)`. Registered tolerances are `D: 1`, `O: 1`, and `L: max(1, ceil(0.05 × original L))`. A tradeoff does not count as ablation survival.

## Aggregation

Retain all mapping-level observations. Do not discard mappings because they fail, remain unresolved, differ structurally, increase complexity, or weaken conclusions. Use conservative preservation aggregation, mapping-success frequency `S_V`, median complexity, full minimum, maximum, and range, separate agreement, majority-based ablation, and registered Pareto rules. Do not select the best mapping as the vocabulary-level result.

## Pareto Dominance

A vocabulary dominates another only when preservation is no worse on every comparable dimension, `A_used` is no greater, `A_required` is no greater, `D`, `O`, and `L` are no greater, and at least one difference is strictly and materially better. Unknown preservation blocks dominance on the affected comparison. No weighted aggregate is permitted.

## Constraint Decision Rules

Support `H_{C,G}` only when the target has no worse comparable preservation, no required `Unknown`-blocked comparison, higher `G_s` than both baselines, and is not Pareto-dominated on representation cost. Support `H_{C,R}` only when the target has no worse comparable preservation, no required `Unknown`-blocked comparison, Pareto-dominates both baselines on `R`, has at least one material cost advantage over each, and has no lower `G_s`.

## Secondary Uniqueness Metric

Retain `U` only as a secondary result. A property counts only when directly expressed through vocabulary-origin structure, required for preservation, both baselines fail without equivalent reconstruction, canonicalization and ablation preserve the finding, and at least two adjudicators agree. Do not include `U` in Pareto dominance or primary `H_C` rules.

## Adjudication

Two independent adjudicators are required. A third blinded adjudicator resolves unresolved disagreements. Preserve both original judgments, disputed component, governing rule, final resolution, consensus status, and third-adjudicator involvement.

## Statistical Philosophy

Version 1.0 is decision-theoretic, not population-inferential. Do not add p-values, confidence intervals, null-hypothesis tests, or population-generalized evaluator claims.

## Provenance

Every dataset and artifact must record immutable identifiers for protocol version, scenario version, vocabulary version, instruction version, canonicalization version, adjudication version, experiment, evaluator, assignment, date, ablation condition, adjudicators, automated system or model version, and registered clarifications.
