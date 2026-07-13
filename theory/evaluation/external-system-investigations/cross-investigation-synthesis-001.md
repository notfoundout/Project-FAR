# Cross-Investigation Synthesis 001

Status: provisional

## Scope

This synthesis covers the external-system investigations completed in this pull request:

- Classical Propositional Logic;
- First-Order Predicate Logic;
- Bayesian Reasoning;
- Scientific Method;
- Large Language Model Reasoning;
- Agentic AI Reasoning;
- Human Expert Reasoning;
- Legal Reasoning;
- Analogical Reasoning.

The synthesis does not include older external-system reports except as background. It does not claim universality, necessity, or minimality.

## Recurring FAR/FARA Components

All nine scoped EV-021 through EV-029 investigations required Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus for their target mappings. FARA operational components were used when procedure, update, proof, inquiry trace, agent loop, expert protocol, legal sequence, or analogy mapping process was included.

Recurring mappings:

- Investigation: question, consequence judgment, update objective, or inquiry objective.
- Representation: formulas, models, hypotheses, evidence, data, probabilities, protocols, and conclusions.
- Representational Structure: syntax trees, binding, valuation/model structure, dependency graphs, conditional-dependence relations, experimental designs, and evidence-claim dependencies.
- Interpretation: truth-functional semantics, model-theoretic semantics, probabilistic semantics, measurement semantics, and statistical or operational definitions.
- Reasoning Calculus: truth-table checks, proof rules, semantic consequence, Bayesian update, experimental protocols, statistical analysis, and revision rules.

## Components Never Required

No FAR primitive was never required in this batch. No FARA component was categorically unused when operational preservation was part of the investigation objective. Some static variants could omit operational details, but the methodology required operational preservation review, and each completed investigation used state-transition vocabulary for replay.

## Repeated Preservation Failures

No preservation dimension failed for classical propositional logic or first-order predicate logic. Bayesian reasoning passed for explicit exact or sufficiently specified approximate models, while opaque approximate claims were outside scope. Legal reasoning was classified as a conservative extension. Scientific method, Large Language Model reasoning, Agentic AI reasoning, Human Expert reasoning, and Analogical reasoning produced `unknown` preservation results in one or more dimensions, especially operational preservation, dependency preservation, and information preservation.

## Repeated Ambiguities

Recurring ambiguities were:

- whether a broad family should be investigated as one system or split into narrower subtypes;
- whether an implementation's opaque behavior counts as reasoning process evidence or only output evidence;
- what documentation threshold is sufficient for operational equivalence and long-term reproducibility;
- whether domain-specific policies such as prior selection, approximation diagnostics, replication, and evidence quality should become reusable derived concepts.

## Recurring Methodological Weaknesses

No defect in the external-system investigation methodology was discovered. The methodology did expose practical pressure points:

- very broad systems can be forced into `unresolved` unless scoped to a documented subtype;
- operational equivalence is difficult to evaluate for underdocumented or opaque systems;
- source-evidence retrievability matters materially for empirical and computational systems.

These are execution burdens, not methodology defects, because the methodology provides `unknown`, `unresolved`, and `outside scope` outcomes.

## Candidate Reductions of FAR/FARA

No candidate reduction is supported by this batch. Each investigation used Interpretation and Reasoning Calculus distinctly; syntax-only encodings were repeatedly rejected as insufficient. Representational Structure was necessary to preserve formula structure, quantifier binding, probabilistic dependence, and evidence-claim dependency.

## Candidate Missing Primitives

No candidate sixth primitive was identified. Bayesian reasoning and scientific method introduced pressure for domain-specific policies, but these appeared to be conservative extensions of Interpretation, Representational Structure, Reasoning Calculus, Admissibility Structure, and Resolution Rule.

## Recurring Support for Universality

The formal logic investigations provide positive evidence that two central explicit formal reasoning systems are representable and faithfully preserved. Bayesian reasoning provides positive evidence for explicit quantitative uncertain inference. Scientific method provides partial support for explicit, documented empirical inquiry but also demonstrates that the broad family is not fully classifiable without subtype-specific evidence.

## Recurring Evidence Against Universality

No in-scope candidate primitive failure was found. Evidence against a broad universality reading comes from outside-scope and unresolved cases: opaque Bayesian-like systems, tacit scientific practice, inaccessible data or procedures, and underdocumented empirical inference. These do not refute FAR primitive sufficiency for explicit reasoning, but they do limit the evidence base and prevent universal claims.

## Recurring Evidence Regarding Necessity

Within this batch, all five FAR primitives recur across materially different systems. Interpretation and Reasoning Calculus are especially resistant to collapse: the reports repeatedly distinguish formula encoding from semantics, probability formulas from probabilistic interpretation, and scientific outputs from inquiry procedure. This is evidence of practical necessity for these investigations only, not proof of global necessity.

## Recurring Evidence Regarding Minimality

This batch does not support minimality beyond the negative result that no unused FAR primitive appeared across completed investigations. No ablation, primitive-independence proof, or primitive-elimination experiment was performed. Therefore minimality remains unresolved.

## Answers Limited to Evidence Generated in This Pull Request

### 1. What evidence currently supports the universality hypothesis?

Positive support consists of successful representation and preservation for classical propositional logic and first-order predicate logic, plus conservative-extension representation for explicit Bayesian reasoning. Scientific method adds partial support for documented explicit inquiry but not for the entire general family.

### 2. What evidence currently contradicts it?

No candidate primitive failure was found. However, opaque or underdocumented reasoning processes in Bayesian-like systems and scientific practice cannot be counted as positive evidence; they remain outside scope or unresolved. This contradicts any premature claim that the current investigations establish universality.

### 3. What evidence currently supports minimality?

The batch provides weak practical support only: no FAR primitive was unused across all investigations, and syntax-only or semantics-only reductions were rejected within individual reports. This is not a proof of minimality.

### 4. What evidence currently contradicts minimality?

No direct contradiction was found, but minimality lacks sufficient evidence because no ablation or primitive-elimination test was performed. The need for domain-specific policies in Bayesian reasoning and scientific method may also motivate future tests of whether some FARA structures are derived rather than primitive-level necessities.

### 5. Which questions remain unresolved?

- How should broad families such as scientific method be decomposed into subtype investigations?
- What documentation threshold is sufficient for operational preservation?
- Which domain policies should become reusable derived concepts?
- Can any FAR/FARA component be ablated without loss for one or more investigated systems?
- How should opaque AI or tacit expert reasoning be evaluated when only outputs are accessible?

### 6. Based only on the investigations completed so far, which allowable conclusion is currently best supported?

The best-supported allowable conclusion is that available evidence remains insufficient for universality, necessity, or minimality acceptance: several explicit reasoning systems are representable without a candidate sixth primitive, but unresolved preservation and absent ablation evidence prevent a stronger conclusion.


## Comparative Analysis After Adversarial Investigation Batch

The second batch deliberately targeted systems most likely to expose limits: opaque machine learning, dynamic tool-using agents, tacit human expertise, institutional legal reasoning, and underdetermined analogy. The accumulated classifications are now: three `fits FAR`-style formal systems in the broader registry background, two `fits FAR` investigations in this PR, three `conservative extension` or extension-pressure investigations in this PR, and four `unresolved` investigations in this PR. No `candidate primitive failure` has been found in this PR.

### Components Required by Every Investigated Reasoning System

Every completed PR investigation required, at minimum, Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus for the scoped target. FARA state-transition components were required whenever the investigation objective included procedure replay, update, proof trace, agent loop, expert protocol, legal reasoning sequence, or analogy mapping process.

### Components Never Required Across All Completed Investigations

No FAR primitive was unused across all completed investigations. No FARA component was shown to be globally unnecessary, although static descriptions can sometimes omit transition details when operational preservation is outside the scope. This is not minimality evidence sufficient for acceptance because no ablation proof or primitive-elimination experiment was performed.

### Recurring Preservation Failures

No formal preservation failure became a candidate primitive failure. Recurring `unknown` preservation results occurred in operational, dependency, and information preservation for LLM reasoning, agentic AI, human expert reasoning, scientific method, and analogical reasoning. These failures were caused by inaccessible internals, mutable external dependencies, underdocumented procedures, tacit cognition, or underspecified relevance criteria.

### Recurring Conservative Extensions

Recurring conservative extensions include quantitative probability policy, empirical-study protocol policy, model/run provenance, tool and environment schemas, memory policies, jurisdiction and authority hierarchy, defeasible argument status, standards of review, source-target mapping constraints, similarity metrics, and relevance criteria. These extend interpretation, representational structure, reasoning calculus, admissibility, and resolution rules rather than indicating a sixth primitive.

### Recurring Ambiguities

Recurring ambiguities are broad-family scope, accessibility of hidden processes, sufficiency of replay artifacts, distinction between generated explanation and actual process, treatment of tacit knowledge, mutable external dependencies, and objective criteria for discretionary or relevance-sensitive judgments.

### Recurring Methodological Weaknesses in the Adversarial Batch

No methodology defect requiring modification was discovered. The methodology repeatedly forced uncertainty to be recorded as `unknown`, `unresolved`, or `outside scope` instead of allowing ad hoc reinterpretation. The main execution burden is that high-risk systems require artifact bundles richer than ordinary publications or logs often provide.

### Candidate Reductions

No candidate reduction is currently supported. The adversarial batch reinforced the separation between syntax and semantics, output and process, process and dependency provenance, and representation and faithful representation.

### Candidate Missing Primitives After the Adversarial Batch

No candidate missing primitive is currently supported. The strongest pressures are not new primitive types but evidence-access and domain-policy requirements. A future candidate primitive failure would need an explicit in-scope reasoning process that cannot be represented as investigation, representation, structure, interpretation, calculus, or conservative extension of those roles.

### Strongest Evidence Supporting Universality

The strongest support remains successful preservation of formal logic systems and conservative-extension mappings for Bayesian and legal reasoning. The adversarial batch adds limited support by showing that even complex institutional and interactive systems have visible artifacts naturally mapped to existing components when sufficiently documented.

### Strongest Evidence Contradicting Universality

The strongest contradictory evidence is not a primitive failure but a major evidential limitation: LLMs, agentic AI, human expertise, scientific practice, and analogy often cannot be faithfully preserved from ordinary evidence because crucial process, dependency, or information artifacts are inaccessible or under-specified. This contradicts any claim that the current evidence establishes universality.

### Strongest Evidence Supporting Necessity

Across all completed investigations, every FAR primitive recurs. Interpretation and Reasoning Calculus are especially necessary in practice because syntax-only encodings fail for logic semantics, probabilistic updating, scientific inference, LLM outputs, legal authority, and analogy relevance. Representational Structure is repeatedly required for dependency, binding, context, authority hierarchy, and source-target mapping.

### Strongest Evidence Contradicting Necessity

No direct contradiction of component necessity was found, but necessity remains unproved because recurrence in cases is not ablation. Some FARA components may be derived or optional for static-only investigations and require targeted reduction tests.

### Strongest Evidence Supporting Minimality

Only weak practical support exists: no FAR primitive has been globally unused, and several attempted reductions to output-only, syntax-only, rule-only, or explanation-only mappings failed preservation review.

### Strongest Evidence Contradicting Minimality

The evidence contradicts any strong minimality claim because no ablation, independence proof, or primitive-elimination experiment has been completed in this PR. Conservative extensions also raise the question whether some operational machinery should be treated as reusable derived concepts rather than primitive-level requirements.

## Updated Evidence-Limited Answers

### Updated Answer 1 — Evidence Supporting the Universality Hypothesis

The PR evidence supports scoped representability for explicit formal systems and conservative-extension representability for several complex domains, especially Bayesian and legal reasoning. The adversarial investigations show no candidate sixth primitive despite testing opaque, interactive, tacit, normative, and analogical systems.

### Updated Answer 2 — Evidence Contradicting the Universality Hypothesis

No in-scope candidate primitive failure was discovered. The main contradiction is evidential: several important reasoning systems cannot yet be faithfully preserved from available artifacts, so the current evidence does not establish universality and leaves broad classes unresolved.

### Updated Answer 3 — Evidence Supporting Minimality

Only weak operational evidence supports minimality: all FAR primitives recur, and reductions to mere syntax, output, or explanation fail preservation checks in multiple investigations. This is not sufficient for a minimality claim.

### Updated Answer 4 — Evidence Contradicting Minimality

Minimality is contradicted as an accepted conclusion by absence of direct ablation or primitive-independence evidence. No completed investigation proves that every component is globally irreducible.

### Updated Answer 5 — Remaining Unresolved Questions

Highest expected-value unresolved questions are: primitive-ablation replay across one direct-fit and one conservative-extension case; controlled documentation-threshold testing on one unresolved case; formal independence or elimination proof obligations for each FAR primitive; blind duplicate classification of one existing investigation; and, only where these tests cannot resolve the issue, a targeted instrumented replay such as open-weight LLM or fully logged agent reasoning.

### Updated Answer 6 — Best-Supported Allowable Conclusion

The best-supported allowable conclusion remains that available evidence is insufficient. The evidence supports continued investigation of FAR/FARA as a candidate structure for explicit reasoning, but it does not justify universal, necessary, or minimality acceptance.
