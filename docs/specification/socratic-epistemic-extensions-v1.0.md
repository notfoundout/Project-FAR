# Socratic Epistemic Extensions v1.0

Status: Research candidate for governed promotion

This specification defines three additive capabilities for Project FAR: domain-bounded expertise, a consolidated epistemic-boundary object, and an interactive elenchus protocol. It does not alter `PROJECT-FAR-CORE-THEORY-1.1`, FARA's accepted formal kernel, `far-ir/2.0`, `far-ir/2.1`, or the canonical FAR stage sequence. The capabilities are designed to map into existing FAR/FARA/FARO authority rather than create an independent workflow.

## 1. Domain-bounded expertise

A source's competence is proposition-relative and scope-bounded. Evidence that a source is competent in one domain does not transfer automatically to another domain, population, time period, method, or claim type.

A conforming expertise assessment records:

- `source_id`
- `expertise_assertion_id`
- `domain`
- optional `subdomain`
- `claim_types`
- `population_scope`
- `geographic_scope`
- `temporal_scope`
- `method_scope`
- `competence_basis`
- `basis_provenance`
- `assessment_status`
- `uncertainty`
- `limitations`
- `valid_from`
- optional `valid_until`
- `assessor`
- `assessment_method`
- `version`

Allowed assessment statuses are `SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTED`, `INDETERMINATE`, and `NOT_APPLICABLE`.

An expertise assertion never establishes the truth of a substantive claim. It is evidence about whether a source is qualified to contribute on the proposition under evaluation. Applicability must be recomputed for each claim. A system must not infer `expertise(source, Y)` from `expertise(source, X)` merely because X and Y are adjacent domains.

For each source-to-claim use, FAR must create an `EXPERTISE_APPLICABILITY` assessment that states whether the recorded expertise actually covers the claim's domain, scope, method, population, geography, time, and claim type. Missing coverage is `INDETERMINATE` or `INSUFFICIENT_EVIDENCE`, not silent transfer.

## 2. Epistemic-boundary object

FAR already requires scope, nonclaims, `Unknown`, falsifiers, residual uncertainty, limitations, surviving propositions, evidence cutoff, search frame, and closure status. This specification consolidates those existing obligations into one machine-readable terminal object without changing their semantics.

An `EPISTEMIC_BOUNDARY` records:

- `investigation_id`
- `claim_id`
- `claim_version`
- `evidence_cutoff`
- `search_frame`
- `established`
- `conditionally_established`
- `supported_not_established`
- `unknown`
- `not_investigated`
- `not_identifiable_from_current_evidence`
- `explicit_nonclaims`
- `falsifiers`
- `surviving_propositions`
- `residual_uncertainty`
- `limitations`
- `assumptions`
- `closure_status`
- `provenance`
- `boundary_version`

Every non-empty `conditionally_established` entry must identify the assumption or condition on which it depends. Every `unknown` entry must state why it is unknown. `not_investigated` is reserved for matters outside the frozen search contract. `not_identifiable_from_current_evidence` is reserved for questions for which the frozen evidence cannot discriminate among materially distinct states.

The boundary object is a reporting and audit artifact. It does not create new truth semantics or collapse typed claim/evidence/inference assessments into one score.

A closed FAR investigation must be reconstructible from the boundary object plus its referenced underlying artifacts. The boundary object may summarize but may not replace the canonical evidence-closure records.

## 3. Interactive elenchus protocol

The elenchus protocol governs adaptive questioning of a claimant, source author, reviewer, model, or other respondent when the investigation needs to elicit definitions, commitments, assumptions, or inferential warrants.

The protocol is an operation invoked from the canonical FAR workflow. It is not a replacement stage sequence.

Each elenchus session records:

- `session_id`
- `investigation_id`
- `respondent_id`
- `initial_claims`
- `question_events`
- `response_events`
- `commitments`
- `definitions`
- `assumptions`
- `warrants`
- `derived_implications`
- `tensions`
- `contradictions`
- `revisions`
- `withdrawals`
- `unresolved_questions`
- `termination_reason`
- `provenance`
- `session_version`

The protocol follows this loop when applicable:

1. Elicit the exact proposition or definition under examination.
2. Record the respondent's commitment without silently strengthening or normalizing it.
3. Ask consequence-bearing questions that test scope, definitions, assumptions, and warrants.
4. Derive implications only through an explicit stated calculus or inferential rule.
5. Compare derived implications with the respondent's other recorded commitments.
6. Record a `TENSION` when compatibility is uncertain and a `CONTRADICTION` only when incompatibility is demonstrated under the stated interpretation and calculus.
7. Present the conflict or missing premise to the respondent and record the response.
8. Preserve revisions and withdrawals as new versioned commitments; do not overwrite history.
9. Repeat until the relevant commitments are sufficiently explicit for the parent FAR investigation, the respondent declines or cannot answer, the session reaches its declared stopping rule, or further questioning is non-material.

A question must have a recorded purpose such as `DEFINE_TERM`, `FIX_SCOPE`, `EXPOSE_ASSUMPTION`, `TEST_WARRANT`, `TEST_CONSEQUENCE`, `TEST_CONSISTENCY`, `SEEK_COUNTEREXAMPLE`, `DISTINGUISH_INTERPRETATIONS`, or `CLARIFY_REVISION`.

The system must not manufacture a contradiction by substituting a stronger claim, changing the respondent's terminology without provenance, or combining commitments made under materially different contexts without an explicit bridge.

Elenchus produces evidence about the respondent's commitments and the structure among them. It does not establish external factual truth unless the parent investigation separately supplies the required evidence and evaluation.

## 4. Shared invariants

All three capabilities obey the following rules:

1. No capability receives epistemic privilege from being generated by FAR.
2. Every material assessment carries provenance, version, scope, and uncertainty.
3. Missing information remains explicit rather than being completed from model prior or convention.
4. Distinct claim, evidence, inference, expertise-applicability, and closure statuses remain separate.
5. Revisions preserve history and invalidate dependent conclusions when the changed artifact was result-relevant.
6. A machine-readable schema establishes structural conformance only; it does not establish factual correctness or domain adequacy.

## 5. Integration requirements

- Contract Discovery may invoke elenchus to resolve or preserve material ambiguities before freeze.
- Stage 3 interpretation may reference elicited definitions and commitments with session provenance.
- Stage 6 reasoning may use elenchus outputs as explicit premises only at their recorded scope.
- Evidence appraisal may use domain-bounded expertise as one typed input, never as a substitute for direct evidence.
- Evidence Closure must emit or reference one `EPISTEMIC_BOUNDARY` for each terminal claim disposition.
- FARO reporting should expose the epistemic boundary as the compact terminal view while preserving links to the full underlying audit record.
- FARO disagreement analysis may compare expertise-applicability decisions, commitment versions, or epistemic-boundary entries when locating the earliest material divergence.

## 6. Failure conditions

A conforming implementation fails this specification if it:

- transfers expertise across domains or scopes without an explicit applicability assessment;
- treats expertise as proof of the source's substantive claim;
- emits a determinate expertise-applicability status with no provenance or basis;
- omits required terminal uncertainty by leaving an epistemic-boundary category empty without reference to the canonical closure record;
- treats `not investigated` as evidence of absence;
- treats non-identifiability as falsity;
- overwrites an earlier respondent commitment after revision;
- labels two commitments contradictory without recording the interpretation and inferential basis that make them incompatible;
- silently strengthens a respondent's wording during elenchus;
- uses an elenchus response as external factual verification without separate evidence;
- allows any of the three capabilities to bypass the canonical FAR intake, reasoning, evidence-closure, or validation requirements.

## 7. Promotion boundary

This file defines an additive candidate specification. Canonical promotion requires schema/validator conformance, adversarial fixtures, repository health checks, and a governance record showing that the additions preserve the current FAR/FARA/FARO dependency direction and do not silently change core-theory semantics.
