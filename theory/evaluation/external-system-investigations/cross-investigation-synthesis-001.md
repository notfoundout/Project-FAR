# Cross-Investigation Synthesis 001

Status: provisional

## Scope

This synthesis covers the external-system investigations completed in this pull request:

- Classical Propositional Logic;
- First-Order Predicate Logic;
- Bayesian Reasoning;
- Scientific Method.

The synthesis does not include older external-system reports except as background. It does not claim universality, necessity, or minimality.

## Recurring FAR/FARA Components

All four investigations required Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus. All four also used FARA operational components when procedure, update, proof, or inquiry trace was included.

Recurring mappings:

- Investigation: question, consequence judgment, update objective, or inquiry objective.
- Representation: formulas, models, hypotheses, evidence, data, probabilities, protocols, and conclusions.
- Representational Structure: syntax trees, binding, valuation/model structure, dependency graphs, conditional-dependence relations, experimental designs, and evidence-claim dependencies.
- Interpretation: truth-functional semantics, model-theoretic semantics, probabilistic semantics, measurement semantics, and statistical or operational definitions.
- Reasoning Calculus: truth-table checks, proof rules, semantic consequence, Bayesian update, experimental protocols, statistical analysis, and revision rules.

## Components Never Required

No FAR primitive was never required in this batch. No FARA component was categorically unused when operational preservation was part of the investigation objective. Some static variants could omit operational details, but the methodology required operational preservation review, and each completed investigation used state-transition vocabulary for replay.

## Repeated Preservation Failures

No preservation dimension failed for classical propositional logic or first-order predicate logic. Bayesian reasoning passed for explicit exact or sufficiently specified approximate models, while opaque approximate claims were outside scope. Scientific method produced repeated `unknown` preservation results at the general-family level, especially for operational preservation, dependency preservation, and information preservation.

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

The best-supported conclusion is provisional external-validation support with unresolved scope limitations: several explicit reasoning systems are representable without a candidate sixth primitive, but the evidence does not justify a universal, necessary, or minimality claim.
