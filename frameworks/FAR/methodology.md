# FAR Methodology

## Purpose

This document defines the methodology of the Foundational Analysis of Reasoning (FAR).

FAR provides a structured process for conducting investigations within the architectural framework established by FARA.

It defines how the architectural components are applied during an investigation.

This document describes methodological principles.

The canonical ordered stage sequence is maintained in:

`workflow.md`

---

## Objective

The objective of FAR is to conduct contract-explicit investigations that are:

- structured;
- explicit;
- auditable;
- reconstructible.

The methodology is independent of any particular reasoning calculus or application domain.

---

## Methodological Role

FAR does not define the architecture of reasoning.

FAR may apply the representation target supplied by FARA, but adequacy is established only relative to a declared contract and factorization proof.

When a supplied input does not itself constitute an explicit validated comparison-contract artifact, FAR governs the pre-contract discovery and freeze process through the [Contract Discovery Protocol](../../methodology/contract-discovery-protocol.md).

Intake may be bypassed only when the supplied artifact itself is machine-readable, conforms to the applicable downstream contract format and semantic validator, and is recorded by exact format/version and content hash. A prose assertion that the contract is complete is not evidence of completeness.

After substantive evaluation, FAR separately governs investigation stopping through the [Post-Evidence Closure Protocol](../../methodology/post-evidence-closure-protocol.md). An atomic proposition can receive a decisive logical disposition before the surrounding investigation has satisfied bounded evidence-saturation, interpretive-closure, and residual-uncertainty obligations.

FAR does not introduce new primitives.

FAR workflow stages are procedural roles used to organize investigation activity. Construct, Differentiate, and Restrict name actions in that workflow; they are not primitive operators.

---

## Workflow Delegation

A FAR investigation proceeds according to the canonical workflow defined in:

`workflow.md`

This document does not maintain an independent stage list.

Any change to the FAR stage sequence shall be made in `workflow.md` and then reflected in dependent documents.

The contract-discovery intake gate is a precondition on Stage 1 when required; it does not create a second independent stage sequence.

The post-evidence closure gate applies after a logical disposition is recorded when `Resolved` status is sought; it does not create a second reasoning calculus or redefine the Stage 1–9 sequence.

---

## Delegated Architectural Concepts

The following concepts are defined by FARA and repository-wide canonical definitions:

- reasoning state;
- reasoning state representation;
- transition signature;
- Admissibility Structure (Ω);
- resolution rule;
- resolution execution;
- resolution.

FAR specifies how these concepts are used during an investigation.

FAR does not redefine them.

---

## Principles

Every FAR investigation should satisfy the following principles and the contract-relative conformance overlay in `workflow.md`.

### Explicitness

Every assumption, representation, transformation, candidate, admissibility classification, resolution rule, and conclusion should be explicitly represented when relevant.

When input requires contract discovery, every material parse, interpretation, materiality decision, exclusion, synthesis, inference, search boundary, compatibility decision, and candidate-contract parameter provenance that affects construction should also be explicit.

When a logical disposition is recorded, the investigation must separately expose the evidence-search frame, strongest opposing evidence, material alternatives, surviving narrower propositions, measurement or classification limits, and residual uncertainty required by the closure protocol before claiming full resolution.

Silent omission weakens the investigation record.

---

### Source-grounded contract discovery

A result-determining contract choice shall not be filled from convention, familiarity, model prior, unstated preference, or remembered context when the supplied artifact leaves that choice open.

Material source-supported interpretations are retained as separate candidates unless an explicit exclusion records why one is inadmissible at the frozen scope.

Materiality classifications and downstream contract parameters remain traceable rather than becoming new hidden choice points.

The bounded contract family is frozen before evaluation. Evaluation does not choose which supported interpretation counts.

This procedure controls analyst freedom; it does not claim open-world semantic completeness or a uniquely unbiased contract.

---

### Auditability

The complete investigation should be reconstructible from its governed intake when applicable, or from the exact supplied validated downstream contract artifact when intake is legitimately bypassed, together with contract mappings, reasoning states, transition signatures, decoder/collision evidence, revision records, validation status, logical disposition, post-evidence closure evidence, and closure status.

An auditor should be able to distinguish source-explicit content from synthesis and inference, identify every material exclusion, recompute relevant hashes, verify that evaluation followed rather than preceded the governing freeze or supplied validated contract identity, and distinguish a settled proposition from a saturated investigation.

---

### Neutrality

The methodology does not prescribe which reasoning calculus should be used.

Different investigations may employ different calculi.

FAR does not require a specific logic, mathematical system, epistemology, scientific domain, legal standard, historical method, or AI architecture.

Neutrality does not permit silent contract completion. Competing source-supported interpretations remain explicit when they are materially outcome-relevant.

---

### Reconstructibility

A FAR investigation is reproducible to the extent that another investigator can reconstruct the reasoning process from the recorded artifacts under the stated interpretation and reasoning calculus.

FAR does not require that independent investigators reach identical psychological states or identical judgments.

It requires enough explicit structure for the investigation to be reconstructed, audited, and compared.

---

### Iterative Revisability

A FAR investigation may return to earlier workflow stages whenever new representations, revised interpretations, modified criteria, evidence, or additional reasoning require further analysis.

Every such revision should record the stage revisited, the reason for revision, the artifact changed, and the effect on later stages.

A material revision to a frozen intake requires a new freeze and invalidates evaluations bound to the prior discovery hash.

A terminal closure pass that yields a new material finding invalidates full closure until the finding is incorporated and the closure analysis is rerun.

---

### Closure Discipline

Logical disposition and investigation closure are not synonyms.

A proof, counterexample, or other decisive result can settle the exact frozen proposition while leaving the surrounding investigation incompletely searched or interpreted. FAR therefore forbids using `claim settled` as evidence that `investigation complete` unless the separate post-evidence closure gate has passed.

Full `Resolved` status requires bounded evidence-class coverage, opposing evidence review, measurement/data-limit review, applicable denominator/directness/construct checks, material alternatives, surviving narrower propositions, residual uncertainty, interpretive closure, and a terminal pass over the declared search frame that yields zero new material findings.

If those obligations are incomplete, a defensible atomic disposition may be recorded as `Provisionally resolved`, but not promoted to closure-complete `Resolved`.

Closure remains bounded by the declared frame and does not prove that future or undiscovered evidence cannot exist.

When a complete frozen contract family yields divergent exact outcomes, the divergence is preserved as contract sensitivity rather than resolved by selecting a preferred interpretation after evaluation.

---

## Relationship to FARA

FARA defines the architectural components used during an investigation.

FAR defines the methodology for applying those components.

The methodology depends on shared theory and may use FARA, but it does not make FARA a universal ontology. It must report when behavior fails to factor through the selected representation.

---

## Relationship to FARO

FARO should operationalize stable FAR methodology.

FARO should not redefine FAR methodology, alter FAR workflow stages, or introduce replacement primitives.

---

## Current Status

FAR v1.0 remains Stable as the selected Project FAR methodology. The terminal core theory adds a mandatory contract-relative conformance overlay without claiming that the full workflow is uniquely derived.

The accepted contract-discovery intake correction closes a validated application-boundary defect at the bounded procedural level: under-specified input can be carried into the existing contract-relative machinery without silently choosing a result-determining interpretation, while already explicit downstream contracts can bypass intake only through exact artifact identity and successful applicable validation. The correction changes no core-theory claim and does not reinterpret `far-ir/2.0` or `far-ir/2.1`.

The post-evidence closure correction closes a separate stopping-rule defect: a settled atomic proposition no longer licenses full investigation closure without bounded evidence saturation, interpretive closure, surviving-claim analysis, residual-uncertainty recording, and a zero-new-material terminal pass. This correction also changes no core-theory claim and does not reinterpret `far-ir/2.0` or `far-ir/2.1`.

Current post-closure work concerns independent assurance, proof-assistant formalization, contract-schema implementation, domain contracts, approximation/cost objectives, and empirical audit utility under the completed `POST-CLOSURE-001` program and its separately governed successors.
