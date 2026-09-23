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

FAR may use the [Expertise Applicability Protocol](../../methodology/expertise-applicability-protocol.md) when an investigation materially relies on a source's specialized competence. Expertise is assessed separately from substantive claim truth and must be bound to the exact proposition scope in which it is used.

FAR may use the [Elenchus Protocol](../../methodology/elenchus-protocol.md) when an interactive respondent can clarify a material definition, commitment, assumption, warrant, consequence, or revision. Elenchus is a supporting method inside the canonical workflow and does not create a second stage sequence.

FAR does not introduce new primitives.

FAR workflow stages are procedural roles used to organize investigation activity. Construct, Differentiate, and Restrict name actions in that workflow; they are not primitive operators.

---

## Workflow Delegation

A FAR investigation proceeds according to the canonical workflow defined in:

`workflow.md`

This document does not maintain an independent stage list.

Any change to the FAR stage sequence shall be made in `workflow.md` and then reflected in dependent documents.

The contract-discovery intake gate is a precondition on Stage 1 when required; it does not create a second independent stage sequence.

The post-evidence closure contract `FAR-EVIDENCE-CLOSURE-1.0` is defined in `workflow.md`. It governs when a claim-level logical disposition may be promoted into `Resolved` or `Provisionally resolved` investigation closure; dependent documents may validate or operationalize that contract but shall not maintain an independent closure definition.

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

When expertise materially affects evidence appraisal, the claimed competence, its basis, its scope, and its applicability to the exact proposition should be explicit. When interactive questioning materially affects interpretation or reasoning, the questions, responses, commitments, revisions, and inferential rules should be explicit.

Silent omission weakens the investigation record.

---

### Source-grounded contract discovery

A result-determining contract choice shall not be filled from convention, familiarity, model prior, unstated preference, or remembered context when the supplied artifact leaves that choice open.

Material source-supported interpretations are retained as separate candidates unless an explicit exclusion records why one is inadmissible at the frozen scope.

Materiality classifications and downstream contract parameters remain traceable rather than becoming new hidden choice points.

The bounded contract family is frozen before evaluation. Evaluation does not choose which supported interpretation counts.

When an interactive respondent is available, elenchus evidence may clarify a material parse or interpretation before freeze. The dialogue does not authorize silent selection: materially distinct interpretations that survive questioning remain governed by the Contract Discovery Protocol.

This procedure controls analyst freedom; it does not claim open-world semantic completeness or a uniquely unbiased contract.

---

### Expertise scope discipline

A source's competence is not a transferable truth credential.

When expertise is materially relied upon, FAR distinguishes:

1. evidence that the source possesses competence within a recorded scope;
2. whether that scope applies to the exact proposition under evaluation;
3. what the source actually asserts;
4. whether independent evidence supports the substantive claim.

Competence in one domain, subdomain, population, geography, time period, claim type, or method does not silently transfer to a materially different one. Any bridge across different recorded scope values must be explicit and challengeable.

Expertise applicability may inform evidence appraisal under a declared protocol. It cannot replace direct evidence where direct evidence is required, repair an invalid inference, erase counterevidence, or establish substantive truth by status alone.

---

### Interactive commitment discipline

When elenchus is used, a respondent's commitment is recorded before it is tested.

FAR may not silently strengthen, normalize, merge, or rewrite a commitment to create a cleaner argument or contradiction. Derived implications identify their premises, reasoning calculus, and rule. Apparent incompatibility remains a tension or unresolved question until the recorded interpretation and calculus demonstrate contradiction.

A revision creates a new versioned commitment and preserves the earlier one. A withdrawal preserves the withdrawn commitment and its provenance. A later change invalidates dependent reasoning to the extent required by the ordinary FAR revision rules.

Conversational consistency or inconsistency is evidence about the respondent's commitment structure. It is not external factual verification.

---

### Auditability

The complete investigation should be reconstructible from its governed intake when applicable, or from the exact supplied validated downstream contract artifact when intake is legitimately bypassed, together with contract mappings, reasoning states, transition signatures, decoder/collision evidence, revision records, validation status, claim-level logical dispositions, evidence-closure records, and closure status.

An auditor should be able to distinguish source-explicit content from synthesis and inference, identify every material exclusion, recompute relevant hashes, verify that evaluation followed rather than preceded the governing freeze or supplied validated contract identity, and determine whether the evidence-closure gate was satisfied independently of the atomic verdict.

When expertise or elenchus materially affects the investigation, the auditor should also be able to reconstruct the exact competence scope/applicability decision or the exact question-response-commitment-revision chain that influenced the result.

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

A FAR investigation may return to earlier workflow stages whenever new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

Every such revision should record the stage revisited, the reason for revision, the artifact changed, and the effect on later stages.

A material revision to a frozen intake requires a new freeze and invalidates evaluations bound to the prior discovery hash.

A terminal evidence-saturation pass that discovers new material evidence, a new claim decomposition, a new alternative explanation, or a new residual-uncertainty item also reopens the affected reasoning/search work. The investigation may retain any earlier atomic verdict that remains justified, but it may not retain a closure status whose prerequisites no longer hold.

---

### Closure Discipline

A FAR investigation should not simply stop without status.

Closure should be recorded as resolved, provisionally resolved, unresolved, suspended, incomplete, or invalid.

Closure status is methodological rather than truth-guaranteeing.

A claim-level logical disposition and an investigation closure status are separate. A decisive witness, counterexample, proof, authoritative record, or other sufficient atomic evidence may justify a claim verdict before the surrounding investigation is ready to close.

`FAR-EVIDENCE-CLOSURE-1.0` requires bounded post-disposition evidence saturation before `Resolved` or `Provisionally resolved` closure. The investigation must cover its registered applicable evidence/search classes; check denominator, estimand, comparison class, mechanism/directness, measurement, classification, provenance, and ascertainment issues where material; seek the strongest support and strongest counterevidence; test material alternative explanations; preserve narrower surviving propositions and residual uncertainty; complete a terminal bounded saturation pass; and pass the methodology audit.

The closure search remains bounded by the declared search frame, evidence cutoff, and stopping rule. Passing the closure gate does not establish open-world completeness.

When a complete frozen contract family yields divergent exact outcomes, the divergence is preserved as contract sensitivity rather than resolved by selecting a preferred interpretation after evaluation.

After closure, FARO may materialize the recorded justification boundary as an epistemic-boundary view. That downstream reporting object does not become a FAR closure prerequisite and cannot alter the underlying claim or closure status.

---

## Relationship to FARA

FARA defines the architectural components used during an investigation.

FAR defines the methodology for applying those components.

The methodology depends on shared theory and may use FARA, but it does not make FARA a universal ontology. It must report when behavior fails to factor through the selected representation.

Expertise-applicability and elenchus records are expressible with existing identity-bearing representations, relations, states, transitions, and provenance. Their adoption does not establish a new primitive.

---

## Relationship to FARO

FARO should operationalize stable FAR methodology.

FARO should not redefine FAR methodology, alter FAR workflow stages, or introduce replacement primitives.

The epistemic-boundary operation is downstream materialization over already-governed FAR closure information. FAR does not depend on that view.

---

## Current Status

FAR v1.0 remains Stable as the selected Project FAR methodology. The terminal core theory adds a mandatory contract-relative conformance overlay without claiming that the full workflow is uniquely derived.

The accepted contract-discovery intake correction closes a validated application-boundary defect at the bounded procedural level: under-specified input can be carried into the existing contract-relative machinery without silently choosing a result-determining interpretation, while already explicit downstream contracts can bypass intake only through exact artifact identity and successful applicable validation. The correction changes no core-theory claim and does not reinterpret `far-ir/2.0` or `far-ir/2.1`.

The accepted evidence-closure correction adds `FAR-EVIDENCE-CLOSURE-1.0` to prevent a correct atomic adjudication from being treated as proof that the broader investigation has completed its bounded evidence search. It changes closure discipline only; it changes no core-theory claim and does not reinterpret `far-ir/2.0`, `far-ir/2.1`, or the pre-contract intake semantics.

The expertise-applicability and elenchus additions are bounded methodology extensions: the former prevents domain competence from silently leaking into an unrelated proposition, while the latter makes interactive clarification and commitment revision reconstructible. Neither changes the canonical stage sequence or creates a new FARA primitive.

Current post-closure work concerns independent assurance, proof-assistant formalization, contract-schema implementation, domain contracts, approximation/cost objectives, and empirical audit utility under the completed `POST-CLOSURE-001` program and its separately governed successors.
