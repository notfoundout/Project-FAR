# Epistemic Extensions Acceptance and Promotion Record v1.0

Status: **Accepted internal methodology/operation extension**  
Program: `FAR-EPISTEMIC-EXTENSIONS-001`  
Accepted contracts: `FAR-EXPERTISE-APPLICABILITY-1.0`, `FAR-ELENCHUS-1.0`, `FARO-EPISTEMIC-BOUNDARY-1.0`

## Decision

Project FAR accepts three additive capabilities at bounded internal scope:

1. proposition-relative expertise assertions and applicability assessments;
2. an interactive elenchus protocol for versioned commitments, definitions, assumptions, warrants, implications, tensions, contradictions, revisions, and withdrawals;
3. a derived FARO epistemic-boundary view over already-governed FAR closure artifacts.

The accepted change does not alter `PROJECT-FAR-CORE-THEORY-1.1`, the Accepted FARA formal kernel, the canonical FAR stage sequence, `far-ir/2.0`, or `far-ir/2.1`.

## Reduction result

The research pass rejected expansion to three new primitives.

- Expertise applicability is selected evidence-appraisal methodology over existing identities, scopes, relations, provenance, and status records.
- Elenchus is selected interactive methodology over existing representations, reasoning, transitions, revision, and provenance.
- The epistemic boundary is a downstream FARO materialized view over existing FAR scope, nonclaim, uncertainty, assumption, falsifier, limitation, surviving-proposition, and closure information.

The dependency direction remains `foundations → shared theory → FARA → FAR → FARO`.

## Acceptance evidence

The implementation package contains:

- the research reduction at `research/socratic-epistemic-extensions/README.md`;
- `docs/specification/socratic-epistemic-extensions-v1.0.md`;
- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`;
- positive fixtures under `tests/fixtures/socratic-epistemic-extensions/`;
- adversarial regression tests in `tests/test_socratic_epistemic_extensions.py` and focused hardening regressions under `tests/test_socratic_epistemic_*`;
- separately coded internal reference oracles in the replication and focused hardening tests;
- the FAR expertise and elenchus methodology protocols;
- the FAR dependency graph integration;
- the FARO epistemic-boundary operation contract and reporting integration.

Historical promotion-time evidence includes Repository Health run `35823890725`, which passed on implementation/integration head `3ffb530de13b6786b6b06f2d5ede05d1bcfed5a1` after the record-type schema dispatcher was replaced with an explicit discriminated `oneOf`. That run records the evidence available at that stage; it is not the authority for later branch heads.

Subsequent implementation hardening does not silently expand the accepted scope. Pre-merge readiness is re-evaluated by the repository's `Exact Head Assurance` workflow and required `merge-authority` check on the actual pull-request head. Those exact-head CI records, rather than a commit SHA frozen into this document, establish current merge readiness. Promotion into protected `main` remains subject to branch protection and human merge authorization; this acceptance record does not bypass those controls.

## Required behavior

### Expertise

A competence claim must remain bounded to its recorded domain, optional subdomain, claim type, population, geography, time, and method. Every material use against a proposition requires an explicit applicability record. A different recorded scope cannot be marked `MATCH` without an explicit non-empty bridge. Fully `SUPPORTED` applicability cannot hide a partial, mismatched, or unknown material dimension.

Each applicability record binds an exact `expertise_assertion_id` plus `expertise_assertion_version` to an exact `claim_id` plus `claim_version`. Before use, the parent investigation resolves those source revisions and verifies that the recorded IDs, versions, and copied scopes match them. Stable IDs alone do not authorize reuse after a source revision changes.

Expertise applicability is never substantive proof of the source's claim.

### Epistemic boundary

The boundary object consolidates established, conditionally established, supported-but-unestablished, unknown, not-investigated, non-identifiable, and explicit-nonclaim entries with their bases. Conditional entries preserve conditions; unknown/out-of-scope/non-identifiable entries preserve reasons; closed views reference the canonical FAR closure record.

Falsifiers, surviving propositions, residual-uncertainty items, limitations, and assumptions are individually materialized as statement-plus-basis entries. Record-level provenance cannot substitute for the per-item basis mapping.

The view is downstream reporting. It cannot replace or modify FAR closure semantics.

### Elenchus

Questions and responses are event-linked. Commitments preserve exact wording and context. Definitions, assumptions, warrants, and tensions are typed identified records linked to the commitments that support or motivate them; they are not free-form annotation buckets.

Derived implications identify premises, calculus, rule, and implication context. A premise whose commitment context differs from the implication context requires an explicit bridge tied to that premise. A bridge for a non-premise or multiple bridges for one premise is invalid. A recorded bridge makes context transport explicit and auditable; it does not prove that the transport is substantively sound.

A contradiction identifies the compared commitments, interpretation, calculus, and basis.

Revisions create new commitment versions and retain prior history. Every commitment marked `REVISED` is the source of exactly one revision; a revision source cannot fork, a target cannot be reused, the response event authorizing the revision is the source event of the replacement commitment, and that response may not predate the response that sourced the superseded commitment. Withdrawals do not delete prior commitments; every commitment marked `WITHDRAWN` has exactly one corresponding withdrawal event, and the withdrawal response may not predate the response that sourced the withdrawn commitment.

Elenchus establishes facts about the recorded commitment structure only. Timestamp ordering establishes internally possible record chronology only; it does not establish external wall-clock accuracy or causality. External factual claims still require the parent FAR investigation's evidence.

## Failure conditions preserved by tests

The implementation fails closed on, among other cases:

- cross-domain or cross-scope expertise marked fully applicable without a bridge;
- dimension values inconsistent with their recorded scopes;
- empty strings used as expertise bridges or other nullable scope placeholders;
- missing expertise-assertion or claim revision bindings in applicability records;
- resolver-supplied source revisions whose IDs, versions, or scopes do not match the applicability record;
- the same scoped boundary statement silently occupying incompatible categories;
- closed boundary views without closure-record linkage;
- unknown/conditional records missing required reasons or conditions;
- falsifiers, surviving propositions, residual uncertainty, limitations, or assumptions lacking item-level basis references;
- responses or commitments referencing nonexistent events;
- definitions, assumptions, warrants, tensions, implications, revisions, withdrawals, or contradictions referencing nonexistent commitments;
- free-form elicited records missing required typed content;
- implication context collapse across differently contextualized premises without an explicit per-premise bridge;
- context bridges attached to non-premises or duplicated for one premise;
- revisions overwriting prior commitments or using non-increasing versions;
- a `REVISED` commitment without a revision event;
- a `WITHDRAWN` commitment without a withdrawal event;
- forked revision sources, reused revision targets, repeated withdrawals, or revision response events that do not source the replacement commitment;
- revision or withdrawal lifecycle responses that predate the response event that sourced the commitment they modify;
- contradictions lacking explicit structure or referencing missing commitments.

The independent boundary replication oracle mirrors the contract's actual exclusivity rule: the same statement is prohibited across incompatible terminal categories, while an identical repeated entry within one category is not silently promoted into a cross-category defect by the oracle alone.

## Assurance boundary

This is internal methodology and implementation assurance. The reference oracles are separately coded inside Project FAR but remain project-authored.

The acceptance does **not** establish:

- that expertise guarantees truth;
- a universal ontology of expertise domains or valid cross-domain bridges;
- that a recorded context bridge is substantively valid merely because it is explicit;
- that the boundary object enumerates all possible unknowns or proves open-world completeness;
- that natural-language contradiction detection is solved by the structural validator;
- that conversational consistency establishes factual truth;
- that recorded timestamp order proves wall-clock accuracy or external causality;
- historical derivation of Project FAR from Socrates;
- external investigator independence;
- empirical utility, comparative superiority, product readiness, novelty, priority, or commercial value.

## Reopening

Reopen or restrict this acceptance if a reproducible counterexample shows that the accepted record formats silently permit one of the prohibited collapses above, or if a later canonical FAR/FARA/FARO change invalidates the recorded dependency mapping.
