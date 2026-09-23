# Epistemic Extensions Research Record

Status: **Research — implementation candidate under validation**  
Investigation: `FAR-EPISTEMIC-EXTENSIONS-001`  
Date: 2026-09-23

The label “Socratic” records the motivating analogy used in the investigation. It does not claim historical derivation of Project FAR from Socrates.

## Question

Does current Project FAR already provide complete, explicit, machine-checkable support for all three of the following operations?

1. deciding whether a source's demonstrated expertise is applicable to the exact proposition under evaluation without allowing competence to transfer silently across domains or scopes;
2. emitting one consolidated terminal artifact that states the exact boundary between what an investigation establishes, conditionally establishes, supports without establishing, leaves unknown, does not investigate, cannot identify from the frozen evidence, and explicitly does not claim;
3. conducting an adaptive commitment-elicitation dialogue that preserves definitions, assumptions, warrants, consequences, tensions, demonstrated contradictions, revisions, withdrawals, and provenance without creating an independent FAR workflow.

## Execution

Current authority was traced through the research execution charter, canonical map, project status, Research Doctrine, Contract Discovery Protocol, FAR workflow, FAR investigation validation, Evidence-Closure correction, FARO operation taxonomy/interface/reporting/disagreement analysis, `far-ir/2.0`, the limitations register, and Saturation Baseline v0.5.

The three candidate additions were then subjected to elimination, reduction, and consolidation before expansion.

### Expertise applicability

Existing FAR already distinguishes source authority from truth, requires evidence relevance/applicability, preserves scope, and allows domain-specific appraisal. Saturation Baseline v0.5 also proposes domain-specific evidence-quality protocols. These mechanisms can represent the information needed for bounded expertise, so no new FARA primitive or core-theory concept is required.

The remaining operational gap is narrower: no accepted machine-readable record was located that binds a source's competence claim to the exact claim domain, subdomain, claim type, population, geography, time, and method, and then fails closed when those dimensions do not transfer. The candidate therefore adds a typed expertise assertion and a separate proposition-relative applicability assessment.

### Epistemic boundary

Current FAR already requires the information that defines a knowledge boundary: claim scope, nonclaims, typed `Unknown`, falsifiers, surviving propositions, limitations, residual uncertainty, evidence cutoff, search frame, assumptions, and closure status.

Therefore a new epistemic primitive is not justified. The candidate `EPISTEMIC_BOUNDARY` is a derived FARO reporting view that consolidates those existing obligations and links back to the canonical closure record. It may summarize those records but cannot replace or reinterpret them.

### Elenchus

Current FAR can record interpretations, assumptions, reasoning states, transitions, contradictions, challenges, revisions, and alternative explanations. Contract Discovery can preserve ambiguous parses and interpretations. FARO can execute and report operations.

No accepted protocol was located for an interactive respondent loop that elicits a commitment, asks a purpose-typed question, records the answer, derives consequences under an explicit calculus, compares those consequences with recorded commitments, distinguishes unresolved tension from demonstrated contradiction, and preserves revisions without overwriting the original commitment.

The missing capability is procedural rather than architectural. The candidate therefore defines elenchus as an optional FAR-supporting methodology/operation invoked from the existing workflow. It does not create a new stage sequence and does not establish external factual truth from a respondent's answers.

## Observation

All three requested capabilities can be added without changing `PROJECT-FAR-CORE-THEORY-1.1`, the Accepted FARA kernel, the FAR stage sequence, or `far-ir/2.x` semantics.

The smallest defensible additions are:

- one bounded expertise/applicability record family;
- one derived epistemic-boundary reporting object;
- one optional elenchus protocol over existing representations, commitments, reasoning and provenance.

This is strictly smaller than adding three new primitives or a parallel reasoning architecture.

## Discovery

The three gaps are independent at the operational level but share one epistemic rule: a system must make the limits of a justification explicit at the point where a source, conclusion, or dialogue step is used.

`FAR-EPISTEMIC-EXTENSIONS-001` therefore proposes three versioned contracts:

- `FAR-EXPERTISE-APPLICABILITY-1.0` — competence is proposition-relative and scope-bounded;
- `FARO-EPISTEMIC-BOUNDARY-1.0` — terminal knowledge boundaries are a derived view over existing FAR closure semantics;
- `FAR-ELENCHUS-1.0` — adaptive questioning preserves commitments and only records contradiction when an explicit interpretation and calculus demonstrate incompatibility.

## Falsification conditions

The candidate should be rejected or reduced further if any of the following is demonstrated:

- an existing Accepted machine-readable record already enforces proposition-relative expertise applicability across all material scope dimensions;
- the epistemic-boundary view cannot be derived without introducing new truth semantics;
- elenchus requires a new FARA primitive rather than existing representations, relations, transitions and provenance;
- the proposed validator accepts cross-domain expertise as fully supported without an explicit bridge;
- the proposed boundary object permits one identical scoped statement to occupy incompatible terminal categories silently;
- the proposed elenchus record permits revision by overwriting the earlier commitment or permits contradiction without an explicit basis and calculus.

## Implementation evidence

The candidate implementation consists of:

- `docs/specification/socratic-epistemic-extensions-v1.0.md`;
- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`;
- positive conformance fixtures under `tests/fixtures/socratic-epistemic-extensions/`;
- adversarial regression tests in `tests/test_socratic_epistemic_extensions.py`.

The semantic validator intentionally checks only relationships decidable from an explicit record. It does not infer whether a person truly is an expert, whether a natural-language proposition is true, whether two natural-language commitments actually contradict each other, or whether the recorded search is semantically complete.

## Replication plan

Validation has two layers:

1. JSON Schema checks structural obligations and required provenance fields.
2. A separate semantic validator recomputes cross-field invariants and adversarial tests mutate valid records to require rejection of expertise overreach, boundary-state collapse, missing references, commitment overwrite, invalid revision ordering, and unsupported contradiction records.

Repository-wide health and the canonical test runner must pass before promotion. The resulting assurance is internal implementation replication only; it is not external investigator independence.

## Nonclaims

This investigation does not establish:

- that expertise guarantees truth;
- a universal ontology of expertise domains;
- a universal rule for when adjacent domains are equivalent;
- that the epistemic-boundary categories are new primitive truth values;
- that all ignorance can be enumerated;
- that conversational consistency establishes factual truth;
- that Socrates historically supplied Project FAR's architecture;
- external validation, empirical utility, product readiness, novelty, or commercial value.
