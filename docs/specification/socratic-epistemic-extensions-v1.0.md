# Socratic Epistemic Extensions v1.0

Status: **Accepted — bounded internal implementation specification**  
Research basis: `FAR-EPISTEMIC-EXTENSIONS-001`

This specification defines three additive capabilities for Project FAR: proposition-relative expertise applicability, a consolidated epistemic-boundary view, and an interactive elenchus protocol. The “Socratic” label records the motivating analogy only; no historical derivation claim is made.

The additions do not alter `PROJECT-FAR-CORE-THEORY-1.1`, FARA's accepted formal kernel, `far-ir/2.0`, `far-ir/2.1`, or the canonical FAR stage sequence. Elimination and reduction found that all three can be represented using existing FAR/FARA/FARO roles.

## 1. Domain-bounded expertise

Contract: `FAR-EXPERTISE-APPLICABILITY-1.0`.

A source's competence is proposition-relative and scope-bounded. Evidence that a source is competent in one domain does not transfer automatically to another domain, subdomain, claim type, population, geography, time period, or method.

An `EXPERTISE_ASSERTION` records:

- `source_id`;
- `expertise_assertion_id`;
- a `scope` containing `domain`, optional `subdomain`, `claim_type`, `population`, `geography`, `time`, and `method`;
- `competence_basis` and `basis_provenance`;
- `assessment_status`;
- `uncertainty` and `limitations`;
- validity interval;
- assessor, assessment method, and version.

Allowed expertise statuses are `SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTED`, `INDETERMINATE`, and `NOT_APPLICABLE`.

An expertise assertion never establishes the truth of a substantive claim.

For every material source-to-claim use, an `EXPERTISE_APPLICABILITY` record binds the expertise assertion to one exact claim. It preserves both `expertise_scope` and `claim_scope` and assesses domain, subdomain, claim type, population, geography, time, and method separately as `MATCH`, `PARTIAL`, `MISMATCH`, `UNKNOWN`, or `NOT_APPLICABLE`.

A dimension marked `MATCH` despite different recorded values requires an explicit non-empty bridge. Mere adjacency of domains is not a bridge. Overall `SUPPORTED` applicability is invalid if any material dimension is partial, mismatched, or unknown.

Expertise applicability remains distinct from source reliability, evidence quality, evidence relevance, claim status, and inference validity.

## 2. Epistemic-boundary view

Contract: `FARO-EPISTEMIC-BOUNDARY-1.0`.

FAR already requires scope, nonclaims, typed `Unknown`, falsifiers, residual uncertainty, limitations, surviving propositions, evidence cutoff, search frame, assumptions, and closure status. No new epistemic primitive is justified.

`EPISTEMIC_BOUNDARY` is therefore a derived FARO reporting view over those existing records. It contains:

- `investigation_id`;
- `claim_id` and `claim_version`;
- `evidence_cutoff`;
- `search_frame`;
- `closure_record_refs` linking the canonical FAR closure artifacts;
- `established`;
- `conditionally_established`;
- `supported_not_established`;
- `unknown`;
- `not_investigated`;
- `not_identifiable_from_current_evidence`;
- `explicit_nonclaims`;
- `falsifiers`;
- `surviving_propositions`;
- `residual_uncertainty`;
- `limitations`;
- `assumptions`;
- `closure_status`;
- provenance and boundary version.

Every conditional entry identifies its condition references. Every unknown, not-investigated, and non-identifiable entry states why it occupies that category. The same scoped statement may not silently occupy incompatible terminal categories.

The boundary view may summarize canonical FAR records but cannot replace or reinterpret them. FAR closure does not depend on FARO materialization; the dependency direction remains FAR → FARO.

## 3. Interactive elenchus protocol

Contract: `FAR-ELENCHUS-1.0`.

The elenchus protocol governs adaptive questioning of a claimant, source author, reviewer, model, or other respondent when an investigation needs to elicit definitions, commitments, assumptions, or inferential warrants.

The protocol is invoked from the canonical FAR workflow when applicable. It is not a replacement stage sequence.

Each `ELENCHUS_SESSION` records:

- session, investigation, and respondent identity;
- initial claims;
- purpose-typed question events;
- response events linked to the questions that elicited them;
- versioned commitments with exact wording and context;
- typed definitions, assumptions, and warrants, each with stable IDs, exact statements, and commitment references;
- derived implications with explicit premise references, calculus, and rule;
- typed tensions with at least two commitment references and an explicit basis;
- demonstrated contradictions;
- revisions and withdrawals;
- unresolved questions;
- termination reason;
- provenance and session version.

The governed loop is:

1. elicit the exact proposition or definition under examination;
2. record the respondent's commitment without silently strengthening or normalizing it;
3. ask a purpose-typed question directed at scope, definition, assumption, warrant, consequence, consistency, counterexample, interpretation, or revision;
4. materialize result-relevant definitions, assumptions, warrants, and tensions with commitment provenance rather than as free-form annotations;
5. derive implications only through an explicitly named calculus or inferential rule;
6. compare the implications with recorded commitments at compatible contexts;
7. record `TENSION` when incompatibility remains uncertain and `CONTRADICTION` only when incompatibility is demonstrated under an explicit interpretation and calculus;
8. present the conflict or missing premise when further clarification is material;
9. preserve revisions and withdrawals as new events and never overwrite history;
10. require every `REVISED` or `WITHDRAWN` commitment status to be backed by its corresponding event;
11. require every revision or withdrawal response event to occur no earlier than the response event that sourced the commitment it modifies;
12. repeat until sufficient explicitness, respondent refusal/inability, the declared stopping rule, or no further material question.

Question purposes are `DEFINE_TERM`, `FIX_SCOPE`, `EXPOSE_ASSUMPTION`, `TEST_WARRANT`, `TEST_CONSEQUENCE`, `TEST_CONSISTENCY`, `SEEK_COUNTEREXAMPLE`, `DISTINGUISH_INTERPRETATIONS`, and `CLARIFY_REVISION`.

A revision has exactly one source commitment and one replacement commitment. The superseded commitment remains `REVISED`, the replacement has a greater version, the revision response event is the replacement commitment's source event, a revision source may not fork into multiple targets, one target may not be reused by multiple revisions, and the revision response may not predate the response that sourced the superseded commitment. A withdrawal occurs at most once for a commitment, every commitment marked `WITHDRAWN` has a corresponding withdrawal event, and the withdrawal response may not predate the response that sourced the withdrawn commitment.

Elenchus produces evidence about the respondent's commitments and their relations. It does not establish external factual truth unless the parent investigation separately supplies the evidence and evaluation required for that claim.

## 4. Shared invariants

All three capabilities obey these rules:

1. FAR-generated assessments receive no epistemic privilege.
2. Every material assessment carries provenance, version, and scope.
3. Missing information remains explicit rather than being completed from model prior or convention.
4. Claim, evidence, inference, expertise-applicability, and closure statuses remain distinct.
5. Revisions preserve history and invalidate dependent conclusions when the changed artifact was result-relevant.
6. Schema conformance establishes structural consistency only; semantic validation establishes only the explicit cross-field invariants it checks.
7. Neither layer establishes factual correctness, domain adequacy, source truth, semantic completeness, or external validation.

## 5. Integration requirements

- Contract Discovery may use elenchus evidence when an interactive respondent can clarify a material ambiguity. Surviving materially distinct interpretations remain governed by the existing intake protocol.
- If elenchus materially affects pre-freeze Contract Discovery, the exact session or transcript artifact must be registered as a hash-bound `far-intake/1.0` source and any affected parse, interpretation, materiality decision, assumption, or exclusion must use the existing intake provenance rules. The dialogue remains subject to registered search coverage, the terminal source/query saturation recheck, and freeze binding; it is not an intake bypass.
- Stage 3 may reference elicited definitions and interpretations with elenchus provenance.
- Stage 6 may use elicited commitments as premises only at their recorded scope and context.
- Evidence appraisal may use expertise applicability as one typed input; it never substitutes for direct evidence or repairs an invalid inference.
- After a FAR closure record exists, FARO reporting may materialize an `EPISTEMIC_BOUNDARY` as a derived view. FAR itself does not depend on that downstream view.
- FARO disagreement analysis may compare expertise-applicability decisions, commitment versions, or epistemic-boundary entries when locating a material divergence.

## 6. Machine validation

Machine-readable records use format `socratic-epistemic-extensions/1.0` under:

- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`.

The validator fails closed on decidable defects including:

- scope values that do not match their applicability assessments;
- an unbridged `MATCH` across different expertise and claim values;
- fully `SUPPORTED` expertise applicability with a material partial/mismatched/unknown dimension;
- one identical scoped boundary statement placed in incompatible terminal categories;
- response, commitment, elicited-record, implication, revision, withdrawal, or contradiction references to missing objects;
- free-form elenchus definition/assumption/warrant/tension objects that omit their required typed content and provenance links;
- revision that overwrites the old commitment rather than creating a new one;
- non-increasing revision versions;
- `REVISED` or `WITHDRAWN` commitment statuses with no corresponding event;
- revision-source forks, revision-target reuse, repeated withdrawals, or a revision response event that does not source the replacement commitment;
- revision or withdrawal response events that predate the response event that sourced the commitment they modify;
- malformed, timezone-naive, or inverted expertise validity intervals;
- malformed or timezone-naive elenchus event timestamps, or a response that predates its linked question.

Natural-language expertise, truth, entailment, contradiction, or completeness are outside the validator's decidable scope. Lifecycle chronology establishes only internally possible recorded ordering; it does not prove wall-clock accuracy or external causality.

## 7. Failure conditions

A conforming implementation fails this specification if it:

- transfers expertise across a material scope difference without an explicit applicability assessment;
- treats expertise as proof of the source's substantive claim;
- fabricates an applicability bridge;
- treats `not_investigated` as evidence of absence;
- treats non-identifiability as falsity;
- allows the derived boundary view to replace canonical FAR closure artifacts;
- uses result-relevant pre-freeze elenchus evidence without registering the exact dialogue artifact and its downstream effects through governed intake provenance;
- stores result-relevant definitions, assumptions, warrants, or tensions without explicit commitment provenance;
- overwrites an earlier respondent commitment after revision;
- permits a `REVISED` or `WITHDRAWN` status without the corresponding event;
- permits a revision source to fork, a target to be reused, a withdrawal to be duplicated, or a replacement commitment to cite a different source event from its revision;
- permits a revision or withdrawal lifecycle response to predate the response that sourced the commitment it modifies;
- labels commitments contradictory without recording the comparison interpretation, calculus, and basis;
- silently strengthens a respondent's wording;
- treats an elenchus response as external factual verification without separate evidence;
- creates a parallel workflow or reverses the FAR → FARO dependency direction.

## 8. Assurance boundary

The research record provides the elimination/reduction analysis. The implementation is tested by positive fixtures, adversarial mutations, and separately coded internal reference oracles for the central expertise-scope, boundary-exclusivity/closure-linkage, elenchus-provenance/history, and lifecycle-chronology invariants.

That is internal implementation assurance. It does not establish external investigator independence, empirical utility, product readiness, novelty, priority, or commercial value.
