# Epistemic Extensions Research Record

Status: **Research record supporting an Accepted bounded internal methodology/operation extension**  
Investigation: `FAR-EPISTEMIC-EXTENSIONS-001`  
Date: 2026-09-23

The label “Socratic” records the motivating analogy used in the investigation. It does not claim historical derivation of Project FAR from Socrates.

## Question

Does current Project FAR already provide complete, explicit, machine-checkable support for all three of the following operations?

1. deciding whether a source's demonstrated expertise is applicable to the exact proposition under evaluation without allowing competence to transfer silently across domains, scopes, or source revisions;
2. emitting one consolidated terminal artifact that states the exact boundary between what an investigation establishes, conditionally establishes, supports without establishing, leaves unknown, does not investigate, cannot identify from the frozen evidence, and explicitly does not claim while retaining item-level provenance for material boundary details;
3. conducting an adaptive commitment-elicitation dialogue that preserves definitions, assumptions, warrants, consequences, contexts, tensions, demonstrated contradictions, revisions, withdrawals, and provenance without creating an independent FAR workflow.

## Execution

Current authority was traced through the research execution charter, canonical map, project status, Research Doctrine, Contract Discovery Protocol, FAR workflow, FAR investigation validation, Evidence-Closure correction, FARO operation taxonomy/interface/reporting/disagreement analysis, `far-ir/2.0`, the limitations register, and Saturation Baseline v0.5.

The three candidate additions were then subjected to elimination, reduction, and consolidation before expansion.

### Expertise applicability

Existing FAR already distinguishes source authority from truth, requires evidence relevance/applicability, preserves scope, and allows domain-specific appraisal. Saturation Baseline v0.5 also proposes domain-specific evidence-quality protocols. These mechanisms can represent the information needed for bounded expertise, so no new FARA primitive or core-theory concept is required.

The remaining operational gap is narrower: no accepted machine-readable record was located that binds a source's competence claim to an exact versioned claim across domain, subdomain, claim type, population, geography, time, and method, and then fails closed when those dimensions or referenced source revisions do not transfer. The accepted extension therefore adds a typed expertise assertion and a separate proposition-relative applicability assessment with exact assertion/claim revision binding.

### Epistemic boundary

Current FAR already requires the information that defines a knowledge boundary: claim scope, nonclaims, typed `Unknown`, falsifiers, surviving propositions, limitations, residual uncertainty, evidence cutoff, search frame, assumptions, and closure status.

Therefore a new epistemic primitive is not justified. The accepted `EPISTEMIC_BOUNDARY` contract is a derived FARO reporting view that consolidates those existing obligations and links back to the canonical closure record. Materialized falsifiers, surviving propositions, residual uncertainty, limitations, and assumptions retain per-item basis references rather than relying only on record-level provenance. The view may summarize canonical records but cannot replace or reinterpret them.

### Elenchus

Current FAR can record interpretations, assumptions, reasoning states, transitions, contradictions, challenges, revisions, and alternative explanations. Contract Discovery can preserve ambiguous parses and interpretations. FARO can execute and report operations.

No accepted protocol was located for an interactive respondent loop that elicits a commitment, asks a purpose-typed question, records the answer, derives consequences under an explicit calculus and declared context, prevents silent cross-context premise transport, compares those consequences with recorded commitments, distinguishes unresolved tension from demonstrated contradiction, and preserves revisions without overwriting the original commitment.

The missing capability is procedural rather than architectural. The accepted extension therefore defines elenchus as an optional FAR-supporting methodology invoked from the existing workflow. It does not create a new stage sequence and does not establish external factual truth from a respondent's answers.

## Observation

All three requested capabilities can be added without changing `PROJECT-FAR-CORE-THEORY-1.1`, the Accepted FARA kernel, the FAR stage sequence, or `far-ir/2.x` semantics.

The smallest defensible additions are:

- one bounded expertise/applicability record family with exact source-revision binding;
- one derived epistemic-boundary reporting object with item-level provenance;
- one optional elenchus protocol over existing representations, commitments, reasoning and provenance, including explicit implication contexts.

This is strictly smaller than adding three new primitives or a parallel reasoning architecture.

## Discovery

The three gaps are independent at the operational level but share one epistemic rule: a system must make the limits of a justification explicit at the point where a source, conclusion, or dialogue step is used.

`FAR-EPISTEMIC-EXTENSIONS-001` yielded three versioned contracts:

- `FAR-EXPERTISE-APPLICABILITY-1.0` — competence is proposition-relative, scope-bounded, and bound to exact source revisions before use;
- `FARO-EPISTEMIC-BOUNDARY-1.0` — terminal knowledge boundaries are a derived view over existing FAR closure semantics with traceable materialized details;
- `FAR-ELENCHUS-1.0` — adaptive questioning preserves commitments and contexts and only records contradiction when an explicit interpretation and calculus demonstrate incompatibility.

## Falsification conditions

The accepted extension should be reopened, rejected, or reduced further if any of the following is demonstrated:

- an existing Accepted machine-readable record already enforces proposition-relative expertise applicability across all material scope dimensions and exact source revisions;
- the epistemic-boundary view cannot be derived without introducing new truth semantics;
- elenchus requires a new FARA primitive rather than existing representations, relations, transitions and provenance;
- the validator accepts cross-domain expertise as fully supported without an explicit bridge;
- an applicability record can be used after its referenced expertise assertion or claim revision changes without an explicit re-evaluation;
- the boundary object permits one identical scoped statement to occupy incompatible terminal categories silently or permits a materialized detail with no item-level basis reference;
- an elenchus implication silently transports a differently contextualized premise without an explicit premise-specific bridge;
- the elenchus record permits revision by overwriting the earlier commitment, impossible lifecycle chronology, or contradiction without an explicit basis and calculus.

## Implementation evidence

The accepted implementation consists of:

- `docs/specification/socratic-epistemic-extensions-v1.0.md`;
- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`;
- positive conformance fixtures under `tests/fixtures/socratic-epistemic-extensions/`;
- adversarial regression tests in `tests/test_socratic_epistemic_extensions.py`;
- focused review and lifecycle hardening regressions under `tests/test_socratic_epistemic_*`;
- a separately coded internal reference oracle in `tests/test_socratic_epistemic_extensions_replication.py`;
- the accepted expertise-applicability and elenchus protocols;
- `frameworks/FAR/dependency-graph.md` integration;
- the FARO epistemic-boundary contract and reporting integration;
- the governing acceptance/promotion record at `docs/governance/socratic-epistemic-extensions-promotion-v1.0.md`.

The primary single-record semantic validator intentionally checks only relationships decidable from one explicit record. The separate resolver-assisted expertise binding helper checks supplied resolved assertion and claim revisions against an applicability record but does not fetch or infer those source records. Neither mechanism infers whether a person truly is an expert, whether a natural-language proposition is true, whether two natural-language commitments actually contradict each other, or whether the recorded search is semantically complete.

## Validation and replication

Validation has four layers:

1. JSON Schema checks structural obligations and required provenance/version fields.
2. The single-record semantic validator recomputes explicit cross-field invariants and adversarial tests require rejection of expertise overreach, boundary-state collapse, missing references, cross-context implication collapse, commitment overwrite, invalid revision ordering, impossible lifecycle chronology, and unsupported contradiction records.
3. Resolver-assisted expertise binding tests require the applicability record's assertion/claim IDs, versions, and copied scopes to match the source revisions supplied by the parent investigation.
4. A separately coded project-authored reference oracle independently recomputes the central expertise-scope, boundary-exclusivity/closure-linkage, implication-context, and elenchus-history invariants. Its boundary exclusivity rule matches production: duplicate text within one category is not by itself a cross-category collision.

Repository-wide health and exact-head assurance are required by ordinary merge governance. The resulting assurance is internal implementation replication only; it is not external investigator independence.

## Nonclaims

This investigation does not establish:

- that expertise guarantees truth;
- a universal ontology of expertise domains;
- a universal rule for when adjacent domains are equivalent;
- that an explicit implication-context bridge is substantively valid merely because it is recorded;
- that the epistemic-boundary categories are new primitive truth values;
- that all ignorance can be enumerated;
- that conversational consistency establishes factual truth;
- that Socrates historically supplied Project FAR's architecture;
- external validation, empirical utility, product readiness, novelty, or commercial value.
