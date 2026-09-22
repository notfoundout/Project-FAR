# Project FAR Saturation Baseline v0.4

Status: **Historical Research / Provisional implementation-planning artifact — preserved for provenance; no Accepted authority**  
Version: `0.4`  
Recorded: `2026-09-22`

## Purpose

This document preserves the first capability-class saturation baseline for a prospective Project FAR evidence-and-reasoning verification system.

When work is explicitly requested against `Saturation Baseline v0.4`, this file is a historical task-scoped planning input only. It has no independent authority and is superseded for new planning work by the later baseline candidate on this branch. Current repository governance, canonical architecture, canonical FAR workflow, and applicable FARO operation contracts remain controlling.

The baseline records the architecture reached after repeated searches across fact checking, computational argumentation, formal reasoning, provenance, evidence synthesis, causal inference, metrology, uncertainty, source-dependence analysis, safety assurance, reproducibility, software supply-chain provenance, research integrity, forecasting, and adjacent disciplines.

The saturation claim is intentionally bounded:

> Repeated targeted and broad searches ceased producing new first-class capability classes and instead produced mechanisms representable by existing extension points.

This is **not** a claim that no future capability class can exist.

## Change-control rule after saturation

Future discoveries do not expand the architecture merely because they are useful or novel.

For every candidate mechanism:

1. Determine whether v0.4 can represent it without changing a first-class primitive, invariant, assurance boundary, or extension interface.
2. If yes, treat it as an implementation, benchmark, validator, adapter, protocol, or optimization candidate.
3. If no, require an explicit architecture-change proposal that identifies the missing capability, supplies evidence that existing v0.4 classes cannot represent it, states the smallest required change, and preserves the Project FAR research/governance lifecycle.

The planning burden of proof therefore reverses within this historical artifact after v0.4: expansion must be demonstrated necessary. This rule does not create repository-wide change-control authority.

## Hard invariants

Every conforming implementation shall preserve these invariants.

1. **Never manufacture certainty upstream.** Downstream verification may increase assurance only within the fidelity and uncertainty bounds inherited from upstream stages.
2. **Never collapse distinct epistemic dimensions.** Truth status, evidence sufficiency, source quality, source independence, interpretation fidelity, inference strength, search completeness, confidence, and decision threshold remain separable.
3. **Every consequential transformation is inspectable.** A material source-to-output transformation must have identity, inputs, outputs, method/version, provenance, and validation state.
4. **Every consequential relationship may itself be challenged.** Relations such as `INTERPRETED_AS`, `SUPPORTS`, `CAUSES`, `SAME_PROPOSITION_AS`, and `DERIVED_FROM` are auditable assertions, not invisible plumbing.
5. **FAR receives no epistemic privilege from being FAR.** FAR's extraction, interpretation, retrieval, inference, adjudication, and synthesis outputs are subject to the same challenge, provenance, uncertainty, and validation discipline as external claims.

A sixth implementation-level security invariant follows from the source model:

6. **Source content is data, never authority.** Untrusted source material cannot directly authorize tools, alter controlling policy, suppress evidence, modify decision thresholds, or override evaluator instructions. Validated facts, citations, entities, hypotheses, and other data extracted from source content may inform a sandboxed planner and thereby change a search plan; quoted or embedded instructions remain non-authoritative.

## Assurance zones

The system must preserve the formalization boundary rather than allowing formal verification to erase semantic uncertainty.

```text
REAL-WORLD / HUMAN CONTENT
          |
          | probabilistic observation / interpretation
          v
SEMANTIC REPRESENTATION
          |
          | formalization boundary
          v
FORMAL / COMPUTATIONAL OBJECTS
          |
          | deterministic verification where applicable
          v
VERIFIED DERIVATIONS
```

A proof of a formalization establishes properties of that formalization. It does not by itself establish that the formalization faithfully captures the source utterance or real-world phenomenon.

## Capability-class boundary

| Layer | First-class capabilities required by v0.4 |
|---|---|
| Source | ingestion, immutable source snapshots, cryptographic hashes, authenticity/provenance, source identity, source status |
| Media | transcript spans, image regions, video frame/time ranges, audio segments, contextual claims |
| Provenance | epistemic lineage, computational lineage, entities/activities/agents, attestations |
| Identity | canonical claims, scoped propositions, entity resolution, claim versions, translations |
| Semantics | interpretation candidates, quantifier/scope handling, definition tracking, formalization fidelity |
| Time | valid time, acquisition time, transaction/record time, corrections, supersession, historical reconstruction |
| Decomposition | atomic claims, parent-child relations, decomposition versions, recomposition checks |
| Typing | empirical/causal/normative/predictive classes; observed/measured/reported/inferred/computed/proven origins |
| Retrieval | support search, falsification search, alternatives, active search, prior-audit reuse |
| Completeness | recall targets, coverage estimates, unseen-evidence estimates, stopping justification |
| Evidence | directness, relevance, entailment, source independence, quality, applicability |
| Methodology | domain-specific risk-of-bias and evidence-quality protocols |
| Measurement | operational definitions, construct validity, units, uncertainty, measurement lineage |
| Statistics | estimands, sensitivity/multiverse analysis, heterogeneity, multiplicity, uncertainty |
| Argumentation | premises, conclusions, warrants, assumptions, schemes, critical questions |
| Inference | typed relations and relation-specific validators |
| Defeasibility | defeaters, rebuttals, underminers, undercutters, justification maintenance |
| Causality | causal-claim/design compatibility, confounding, alternatives, identification |
| Hypotheses | competing explanations, diagnosticity, abductive evaluation |
| Uncertainty | epistemic uncertainty, intervals/sets where appropriate, calibration, abstention |
| Conflict | contradiction-preserving reasoning rather than forced premature resolution |
| Computation | datasets -> transformations -> results -> claims, with rerunnable derivations |
| Formal assurance | proof assistants/solvers where formalization is valid; formalization gap preserved |
| Forecasts | resolution criteria, assumptions, deadline, probability history, scoring |
| Commitments | preregistration/protocol/prediction/method commitments and later deviation analysis |
| Updating | living evidence watches, corrections/retractions, dependency-aware reopening |
| Decisions | epistemic state separated from domain-specific burden/decision thresholds |
| Challenges | objections, responses, unresolved disputes, correction/appeal workflows |
| Humans | human review/override as provenance-bearing events rather than invisible authority |
| Security | hostile-content isolation, prompt-injection resistance, tool isolation, access control |
| Privacy | restricted evidence, disclosure controls, privacy-preserving/proof-carrying verification |
| Evaluation | stage-specific benchmarks, adversarial tests, OOD tests, calibration, failure localization |
| Meta-assurance | explicit assurance case for whether FAR itself performed the audit adequately |
| Synthesis | graph-grounded explanation, qualification preservation, disagreement representation |
| Interchange | ClaimReview, AIF-like exports, PROV, JSON-LD, RO-Crate, APIs/MCP |
| Packaging | reproducible audit bundle containing inputs, hashes, methods, outputs, and validation artifacts |

## Core object model

For finite, explicit Project FAR implementations, the Accepted FARA kernel remains canonical. A typed, versioned epistemic graph may be exposed only as an operational representation or derived view whose mapping to the FARA identity-bearing many-sorted relational structure preserves registered commitments, disjoint carrier distinctions, occurrence identities, Event/State/Rule separations, and admission constraints required by current repository authority. It is **not** globally required to be a DAG. Only derivation subgraphs that require acyclicity should enforce it.

Minimum object families:

```text
SOURCE_ARTIFACT
SOURCE_VERSION
SOURCE_LINEAGE
MEDIA_ANCHOR

UTTERANCE
TRANSLATION
INTERPRETATION
CANONICAL_CLAIM
CLAIM_VERSION
CLAIM_SCOPE

EVIDENCE_ITEM
EVIDENCE_REQUIREMENT
EVIDENCE_SET
SEARCH_PROTOCOL
SEARCH_RUN
SEARCH_COVERAGE
SCREENING_DECISION
SOURCE_DEPENDENCE

ARGUMENT
PREMISE
CONCLUSION
WARRANT
ASSUMPTION
INFERENCE
ARGUMENT_SCHEME
CRITICAL_QUESTION
CHALLENGE
DEFEATER

HYPOTHESIS_SET
ALTERNATIVE_HYPOTHESIS
DIAGNOSTICITY_ASSESSMENT

MEASUREMENT
CONSTRUCT
DATASET
COMPUTATION
RESULT

COMMITMENT
FORECAST
RESOLUTION_CONTRACT

ADJUDICATION
ADJUDICATION_VERSION
DECISION_CONTEXT

PROVENANCE_RECORD
ATTESTATION
VALIDATION_RECORD
ASSURANCE_CASE
HUMAN_INTERVENTION
EVIDENCE_WATCH
```

Relationships that materially affect conclusions must be reified or otherwise carry equivalent audit metadata.

Representative relation types include:

```text
ASSERTED_BY_SOURCE
EXTRACTED_FROM
TRANSLATED_AS
INTERPRETED_AS
SAME_PROPOSITION_AS
DECOMPOSES_TO
RECOMPOSES_AS
DERIVED_FROM
CITES
DEPENDS_ON
SUPPORTS
CONTRADICTS
ASSUMES
CAUSES
CORRELATES_WITH
GENERALIZES_TO
ANALOGOUS_TO
DEFINES_AS
PREDICTS
MEASURES
UNDERCUTS
UNDERMINES
REBUTS
QUALIFIES
SUPERSEDES
COPIED_FROM
SYNDICATED_FROM
```

Each consequential relation must be able to carry, directly or through an associated assertion object:

```text
provenance
evaluator / agent
method / protocol
method version
inputs
context
confidence or uncertainty representation
challenges
validation result
timestamps
supersession/version state
```

## Claim identity and scope

Semantic similarity is candidate generation, not identity proof.

Canonical identity must preserve scope dimensions that can change what evidence establishes the claim. At minimum, claim identity must be able to represent:

```text
subject
predicate
object
quantifier
population
geography
time
measurement / operationalization
modality
comparison class
definition set
```

The system must not silently collapse claims such as:

```text
Crime increased.
Violent crime increased.
Violent crime increased nationally.
Violent crime increased nationally in 2025.
Reported violent crime increased nationally in 2025.
```

because the required evidence differs.

## Interpretation and translation fidelity

A source utterance may map to multiple candidate propositions.

```text
SOURCE -> UTTERANCE -> INTERPRETATION(S) -> CANONICAL CLAIM(S)
```

Interpretation must distinguish at least:

```text
EXPLICIT
IMPLIED
RECONSTRUCTED
BACKGROUND
NORMATIVE
```

Explicit claims require source anchoring. Implied and reconstructed claims require provenance showing the source span plus the additional interpretive step.

Translation is itself an interpretation layer. The original-language utterance, translation method/version, ambiguity notes, and translation-to-claim relation remain challengeable.

## Decomposition and recomposition

Atomic verification does not automatically verify the original claim.

For every material decomposition:

```text
ORIGINAL CLAIM
      |
      v
DECOMPOSITION VERSION
      |
      +--> C1
      +--> C2
      +--> C3
      +--> ...
      |
      v
RECOMPOSITION CHECK
```

The system must test whether the decomposition preserves the proposition's material meaning, quantification, scope, modality, and logical commitments. A failed or uncertain recomposition prevents the atomic results from being promoted as verification of the original claim.

## Claim status, evidence status, and inference status

These are separate state spaces.

A claim may be independently supported even when a speaker's inference to it is invalid:

```text
P: SUPPORTED
Q: SUPPORTED
P -> Q: DOES_NOT_ESTABLISH
```

Likewise, an inference can be conditionally strong while the conclusion lacks sufficient independent evidence.

Minimum claim-status vocabulary should support, where applicable:

```text
SUPPORTED
PARTIALLY_SUPPORTED
CONTRADICTED
UNVERIFIABLE
INDETERMINATE
UNRESOLVED
SCOPE_MISMATCH
TEMPORAL_MISMATCH
DEFINITIONAL_DISPUTE
PREDICTION_PENDING
NORMATIVE
ABSTAIN
```

Evidence sufficiency/appraisal is a separate typed assessment, not a claim-status enum:

```text
SUFFICIENT
PARTIALLY_SUFFICIENT
MIXED_EVIDENCE
INSUFFICIENT_EVIDENCE
NO_EVIDENCE_FOUND
NOT_APPLICABLE
INDETERMINATE
```

Individual evidence items separately preserve relevance, directness, source quality, independence/dependence, applicability, scope/temporal compatibility, and support/contradiction relation state.

Minimum inference assessments should support:

```text
ENTAILS
STRONGLY_SUPPORTS
WEAKLY_SUPPORTS
DOES_NOT_ESTABLISH
REQUIRES_MISSING_PREMISE
CONTRADICTORY
```

No single aggregate truth score may erase these dimensions.

## Open-world evidence discipline

The following states are not equivalent:

```text
SEARCH DID NOT FIND EVIDENCE
EVIDENCE SUPPORTS ABSENCE
CLAIM IS FALSE
```

`NO_EVIDENCE_FOUND` therefore requires a linked `SEARCH_COVERAGE` record rather than being emitted from an opaque retrieval attempt.

## Search completeness and stopping

A deep audit must preserve the search process, not only the citations ultimately selected.

`SEARCH_COVERAGE` must be able to record:

```text
search universe / databases / engines
query set and query versions
date/time cutoff
support-search strategy
falsification-search strategy
alternative-hypothesis search
screening history
inclusion/exclusion reasons
deduplication and lineage collapse
recall target when defined
coverage estimate when estimable
estimated unseen relevant material when estimable
stopping rule / stopping justification
known access limitations
```

Coverage estimates must retain their method and uncertainty. A numeric coverage value must not be fabricated where the search universe does not permit a defensible estimate.

## Source independence and lineage

Displayed source count is not independent evidence count.

The system must preserve source-copying, syndication, common-origin, and citation-lineage relationships where detected or asserted.

```text
SOURCE A ----originates----> claim
   |
   +----copied/syndicated--> B
   |                         |
   |                         +--> C
   |
   +------------------------> D

Displayed sources: 4
Independent evidence lineages: 1
```

Source reliability, evidence quality, evidence relevance, evidence-to-claim support, and source independence remain separate dimensions.

## Evidence requirements and appraisal protocols

Retrieval should be driven by explicit evidence requirements for the claim type.

```text
CLAIM
  |
  v
EVIDENCE REQUIREMENTS
  |
  +--> support search
  +--> falsification search
  +--> alternatives
  |
  v
SCREENED EVIDENCE SET
```

Evidence appraisal is protocolized by evidence/domain type rather than delegated to one universal source-quality prompt.

A protocol can use signalling questions, machine-readable answers, deterministic or rule-assisted preliminary judgments, challenge/review, and explicit non-applicability states.

The design pattern may incorporate domain-specific methods analogous to risk-of-bias and certainty-of-evidence frameworks without silently treating any one domain framework as universal.

## Measurement and construct validity

A reported number and the construct it is used to represent are different objects.

Measurements must be able to preserve:

```text
quantity
value
unit
uncertainty
measurement procedure
operational definition
population
sampling frame
instrument / source
transformation
reference / calibration lineage
time
```

The `MEASURES` relation is auditable. Correctly reproducing a statistic does not establish that the statistic validly operationalizes the claimed construct.

## Statistics

Statistical modules must preserve the estimand and the analysis choices that materially affect the result.

Applicable validators may include:

```text
sampling / selection checks
uncertainty interval checks
multiplicity
heterogeneity
sensitivity analysis
multiverse/specification analysis
publication/reporting bias
registration/protocol comparison
external-validity / transportability checks
```

No universal statistical checklist is implied; applicability depends on the claim and evidence design.

## Argumentation and reasoning regimes

Inference type must be explicit enough to select an appropriate verifier.

Supported regimes include at least:

```text
DEDUCTIVE
DEFEASIBLE
ABDUCTIVE
INDUCTIVE
STATISTICAL
CAUSAL
ANALOGICAL
NORMATIVE
```

Argument reconstruction must preserve premises, conclusion, warrants, assumptions, source-explicit links, reconstructed links, schemes where useful, and critical questions.

A formal or symbolic solver should operate on a typed intermediate representation. A model may extract or propose the representation, but solver success cannot prove the extraction was faithful.

## Defeaters and justification maintenance

Real-world reasoning is not assumed monotonic.

The engine must represent rebutting, undermining, and undercutting attacks and preserve which justification supports which conclusion. New evidence may defeat one justification without globally destroying unrelated conclusions.

Dependency-aware reopening must operate on the exact affected justification and downstream dependency closure.

## Competing hypotheses and diagnosticity

For explanatory claims, the system must not evaluate a hypothesis in isolation when plausible alternatives materially affect evidential interpretation.

A hypothesis set may include an explicit unknown/other alternative.

Evidence evaluation should distinguish simple consistency from diagnosticity. Evidence that is equally expected under competing explanations may carry little discriminating weight.

Where defensible probability inputs exist, modules may expose likelihood ratios, Bayes factors, or posterior updates. FAR must not fabricate numerical priors or universalize Bayesian scoring where the inputs are not defensible.

## Causal verification

Causal claims require a specialized gate rather than a generic `correlation != causation` warning.

The first check is compatibility between claim strength and design strength. Applicable downstream checks can include:

```text
temporal order
association
counterfactual support
confounding
selection
reverse causation
measurement
mediators
alternative causes
transportability
dose-response
mechanism
identification strategy
```

The module must state which checks are applicable and why. Observational association does not automatically justify a causal verb.

## Uncertainty, calibration, and abstention

Model confidence is not equivalent to calibrated epistemic uncertainty.

The system must be able to abstain when adjudication requirements are not met. Correct abstention is a valid result.

Where applicable, uncertainty may use intervals, sets, conformal prediction, belief functions, imprecise probabilities, or other defensible representations. The core requirement is that the representation be explicit, calibrated/evaluated where possible, and not converted into false precision.

Implementations should penalize unjustified certainty more severely than correctly refusing to adjudicate.

## Contradiction tolerance

Conflicting evidence must remain representable without forcing premature resolution or permitting classical explosion.

```text
CLAIM P
  +--> support set
  +--> contradiction set
  +--> unresolved conflicts
```

`MIXED_EVIDENCE` is therefore both an adjudication possibility and a requirement that the reasoning substrate preserve localized inconsistency.

## Computation and derivation provenance

Deterministic and computational claims require explicit derivation lineage:

```text
DATASET
  -> QUERY / FILTER
  -> TRANSFORMATION
  -> CALCULATION
  -> RESULT
  -> INTERPRETATION
  -> CLAIM
```

Every rerunnable activity should preserve exact inputs, code or method identity, parameters, environment where material, output identity/hash, and validation result.

Co-occurrence of inputs and outputs in the same run does not establish dependency between every input-output pair.

## Proof-carrying adjudication

Where possible, an adjudication should carry the strongest independently checkable artifact available for its class.

Examples:

```text
deductive claim  -> formal proof / certificate
calculation      -> executable derivation
quotation        -> source-span anchor
provenance       -> hashes / signatures / attestations
statistical      -> rerunnable analysis
retrieval        -> search and screening log
interpretation   -> source spans plus alternatives
causal           -> identification audit
argument         -> explicit premises / warrant / edge evaluation
```

Not every claim admits mathematical proof. `Proof-carrying` means carrying the strongest appropriate verification artifact, not pretending all epistemic questions reduce to theorem proving.

## Prospective commitments

Commitments made before observing an outcome are first-class objects.

Supported commitment types include:

```text
protocol
preregistration
prediction
promised methodology
declared primary outcome
analysis plan
```

The system must support a later commitment-versus-execution diff capable of identifying changes such as outcome switching, analysis switching, post-hoc exclusions, definition changes, unannounced endpoints, or changed prediction criteria without inferring motive merely from the discrepancy.

## Forecasts and resolution contracts

Forecasts retain history rather than overwriting probability estimates.

A forecast object must be able to preserve:

```text
proposition
probability / forecast state
timestamp
resolution criteria
resolution source
deadline
assumptions
status
```

Resolution status should support at least:

```text
OPEN
RESOLVED_TRUE
RESOLVED_FALSE
AMBIGUOUS
ANNULLED
```

## Bitemporal state and living evidence

The system distinguishes:

```text
VALID_TIME       = when a proposition/status applies in the world
ACQUIRED_AT       = when FAR observed/retrieved/obtained the information
TRANSACTION_TIME  = when FAR recorded the information/state in its governed record
```

Corrections, retractions, superseding versions, and new evidence must not erase earlier states.

An `EVIDENCE_WATCH` may record:

```text
claim_id
search_protocol
last_search
next_search / cadence where applicable
change threshold
reopen condition
retirement condition
```

A material status change to evidence must trigger dependency-aware reopening of affected adjudications rather than rely on manual rediscovery.

## Decision contexts and proof standards

Evidence state is distinct from an action threshold.

The same epistemic graph may support different decision contexts without mutating the underlying evidence assessment.

```text
EPISTEMIC ASSESSMENT
        +
DECISION CONTEXT
        +
STANDARD / THRESHOLD
        =
ACTION-RELATIVE RESULT
```

Decision standards therefore belong in an application/decision layer, not inside the underlying claim truth representation.

## Human interventions and challenges

Human review does not become an invisible source of truth.

A material human intervention should preserve:

```text
reviewer / role
input state
change made
reason
evidence added or removed
timestamp
superseded machine judgment where applicable
```

Challenges, corrections, and appeals are provenance-bearing graph events. Unresolved objections remain visible.

## Hostile-source security boundary

All ingested material is untrusted unless independently promoted by a controlling security mechanism.

Source content must not be able to:

```text
authorize tool calls
change system or repository policy
alter evaluator role
suppress counterevidence
change search requirements
modify decision thresholds
write outside the permitted workspace
exfiltrate secrets
convert quoted instructions into executable instructions
```

Extraction and retrieval components should preserve a hard data/control boundary. Security tests must include indirect and embedded instruction attacks across supported modalities.

## Privacy and restricted evidence

The architecture must permit evidence that cannot be disclosed publicly while preserving auditable access controls and disclosure boundaries.

Where appropriate, implementations may use redaction, confidential execution, zero-knowledge proofs, remote attestation, or other proof-carrying techniques so integrity/provenance can be checked without exposing protected underlying data.

No privacy mechanism may silently convert inaccessible evidence into publicly verifiable substantive truth.

## Evaluation architecture

Evaluation begins before optimization and is stage-specific.

Minimum evaluation families include:

```text
claim detection precision/recall/F1
missed-proposition rate
normalization / interpretation fidelity
claim-identity accuracy
classification macro-F1 where classification is applicable
retrieval Recall@K / high-recall coverage
search-stopping calibration
source-lineage / independence accuracy
evidence relevance precision
evidence-support / contradiction accuracy
scope and temporal compatibility
source attribution correctness
decomposition fidelity / recomposition success
argument-edge precision/recall
hidden-premise agreement
causal/design compatibility
adjudication accuracy and calibration
abstention calibration
citation correctness
provenance completeness
reopening correctness
meta-assurance correctness
expert end-to-end agreement
```

Adversarial fixtures should include, at minimum:

```text
true premise -> exaggerated conclusion
correlation -> causation
relative vs absolute increase
wrong denominator
stale evidence presented as current
local sample -> universal claim
group average -> individual claim
citation chain mismatch
headline stronger than study
out-of-context quotation
definition switching
ambiguous quantifier
cherry-picked time window
prediction presented as fact
normative premise disguised as empirical
hidden motive attribution
copied sources presented as independent
malicious instructions embedded in source content
correct atomic checks after a meaning-changing decomposition
retraction after downstream adjudication
translation ambiguity
```

Benchmark success must not be promoted beyond the benchmark's population, perturbation regime, or evaluation protocol.

## Meta-assurance case

Every adjudication carries a fail-closed reliance state:

```text
EXPLORATORY
EXTERNAL_RELIANCE_PENDING
EXTERNAL_RELIANCE_READY
```

The state defaults to `EXPLORATORY`. An adjudication may enter `EXTERNAL_RELIANCE_READY` only through a recorded promotion transition that identifies the exact adjudication version, validates every applicable assurance requirement, generates or regenerates the assurance case from those validation records, and binds the case to the promoted version. Any content change or newly applicable validation invalidates readiness and returns the affected version to `EXTERNAL_RELIANCE_PENDING`.

External publication, export, API response, package, or downstream reuse that represents an adjudication as FAR-assured must require `EXTERNAL_RELIANCE_READY`. Exploratory runs may omit the full assurance case but must retain sufficient provenance for later revalidation.

The resulting machine-readable or equivalently structured assurance case must answer not only whether the target claim/argument passed, but whether FAR adequately performed the audit.

The assurance case should make explicit claims about at least:

```text
source acquisition and anchoring
interpretation fidelity
claim identity and decomposition fidelity
search coverage and stopping
source independence
method/appraisal applicability
evidence-to-claim adjudication
inference reconstruction and edge checking
uncertainty/calibration
provenance and reproducibility
security boundary
unresolved defeaters and limitations
```

Each assurance claim must point to evidence or validation records. Meta-assurance does not permit circular reliance on a final FAR score.

## Synthesis and explanation

Natural-language output is a view over the graph, not the authority surface.

Synthesis must preserve:

```text
qualifications
scope
uncertainty
disagreement
supporting and contradicting evidence
unresolved alternatives
source lineage
status date / valid-time/acquisition-time/transaction-time boundary
```

A summary must not strengthen a claim beyond the underlying graph.

## Interchange and packaging

The internal schema may be richer than external standards but should support adapters rather than forcing proprietary isolation.

Relevant interchange targets include:

- W3C PROV / PROV-O for entity/activity/agent provenance;
- JSON-LD for graph interchange;
- ClaimReview-compatible exports for fact-check interchange;
- AIF-like argument exports where useful;
- RO-Crate-compatible packaging for reproducible research/audit objects;
- APIs and MCP-compatible surfaces where the runtime supports them.

The preferred portable package is a **FAR Audit Crate** containing enough information to inspect and, where possible, reproduce the audit:

```text
audit/
  source-manifest
  source snapshots / hashes
  transcript / media anchors
  claim graph
  evidence graph
  argument graph
  search logs
  screening decisions
  computations
  adjudications
  challenges
  assurance case
  model / protocol versions
  validation records
  machine-readable exports
```

Software-supply-chain provenance patterns may be reused for computational attestations. Epistemic provenance (`what supports this?`) and computational provenance (`how did FAR produce this?`) remain distinct.

## Historical reference implementation capability map

This numbered sequence is preserved as historical planning material. It is not an independent FAR workflow. `frameworks/FAR/workflow.md` is the sole authority for FAR investigation stages and gates; applicable FARO operation contracts remain authoritative for operations. Any implementation using this historical artifact must map these capabilities into those authorities rather than execute the list as a replacement stage sequence.

A complete reference implementation should expose the following logical capabilities even if some are implemented by shared services:

```text
1. INGEST
   artifact + source identity + provenance + authenticity state

2. ANCHOR
   exact passage / frame / timestamp / region

3. INTERPRET
   utterance -> candidate proposition(s)

4. TYPE
   claim type + epistemic origin

5. CANONICALIZE
   scope-sensitive claim identity

6. DECOMPOSE / RECOMPOSE
   atomic propositions with fidelity check

7. RECONSTRUCT
   premises + conclusions + warrants + assumptions

8. SEARCH
   support + falsification + alternatives

9. SCREEN
   inclusion/exclusion + deduplication + lineage collapse

10. APPRAISE
    domain-appropriate evidence/methodology assessment

11. VERIFY EVIDENCE
    evidence -> proposition

12. VERIFY INFERENCE
    proposition(s) -> proposition

13. SPECIALIZED AUDIT
    causal / statistical / measurement / temporal /
    geographic / definitional / computational / formal

14. PROPAGATE
    dependency-aware consequences without erasing history

15. ADJUDICATE
    multidimensional state with calibrated abstention

16. META-ASSURE
    test whether the audit itself met requirements

17. EXPLAIN
    graph-grounded source-linked synthesis

18. PACKAGE
    reproducible FAR Audit Crate + interchange exports

19. WATCH
    reopen when evidence, source status, dependencies, or commitments change
```

## Implementation extension points

After v0.4, new methods should normally enter through one of these replaceable extension points rather than changing the kernel:

```text
ingestion adapter
media parser
transcriber
translator
claim extractor
interpretation proposer
canonicalization candidate generator
identity validator
decomposition engine
retriever
search planner
stopping estimator
source-lineage detector
appraisal protocol
measurement validator
statistical validator
causal validator
argument/inference validator
formal solver/proof checker
uncertainty/calibration module
forecast scorer
commitment-diff engine
provenance adapter
security scanner
challenge workflow
synthesis renderer
interchange exporter
benchmark/evaluation suite
```

Models, search providers, proof assistants, databases, and renderers should be replaceable. The epistemic invariants should not depend on a particular provider.

## Implementation completion contract

When the user instructs Codex to implement this baseline end-to-end, the following is the intended internally controllable completion target.

Codex must first inspect current repository authority and existing mechanisms. It must reuse accepted/current machinery where it already satisfies a requirement rather than duplicate it.

A merge-ready implementation is complete only when, for every v0.4 capability class that is internally implementable:

1. the requirement is mapped to an existing implementation or a new task-scoped implementation;
2. machine-readable schemas/contracts exist where structure must be enforced;
3. consequential transitions have validator contracts;
4. a reference end-to-end path produces a reproducible audit package;
5. uncertainty, abstention, provenance, versioning, and challenge state survive end to end;
6. hostile-source content cannot become control instructions through the supported path;
7. dependency reopening is tested;
8. decomposition/recomposition fidelity is tested;
9. source-dependence handling is tested;
10. search coverage/stopping records are tested without fabricating coverage estimates;
11. meta-assurance is generated from validation evidence rather than a self-score;
12. representative positive, negative, adversarial, and regression fixtures exist;
13. relevant repository validation/CI passes;
14. documentation states exact implemented scope and nonclaims;
15. the final diff is audited for duplicate concepts, unsupported claim promotion, generated residue, stale references, and unnecessary dependencies.

If a capability requires external data, independent human review, restricted infrastructure, credentials, third-party approval, or evidence the repository cannot internally create, Codex must implement the interface/contract and deterministic fixtures where useful, mark the external dependency explicitly, and must **not** fabricate completion of the external step.

The implementation may not promote this Research / Provisional planning artifact into an Accepted scientific result, methodology, workflow, architecture, or other authority surface without the applicable governed lifecycle. Scientific or empirical claims discovered during implementation remain subject to the repository's governing lifecycle.

## Minimal Codex execution prompt

Once this file exists on the target branch/default branch, the intended minimal instruction is:

> Integrate the requirements in `docs/architecture/saturation-baseline-v0.4.md` under current repository authority, mapping investigation-facing capabilities to the canonical FAR workflow and applicable FARO operation contracts. Do not stop until everything internally actionable is complete, tested, documented, audited, and merge-ready.

`AGENTS.md` and current repository governance remain controlling; this sentence supplies the objective, not an exemption from those controls.

## Nonclaims

This baseline does not establish:

- that every listed capability is novel;
- that Project FAR currently implements the listed product architecture;
- that any implementation is accurate in open-world use;
- that architecture-class saturation is permanent;
- that search coverage can always be assigned a numeric value;
- that source independence can always be identified with certainty;
- that formal proof eliminates interpretation uncertainty;
- that an audit score can replace dimensional evidence;
- that the architecture has external empirical validation;
- that Project FAR has achieved product, deployment, legal, scientific, or commercial readiness;
- external-investigator independence, novelty, priority, or market superiority.

## Reference standards and implementation precedents

These are implementation references, not authorities that override Project FAR governance:

- W3C PROV-O: https://www.w3.org/TR/prov-o/
- RO-Crate 1.3: https://www.researchobject.org/ro-crate/specification/1.3/index.html
- Schema.org ClaimReview: https://schema.org/ClaimReview
- SLSA provenance: https://slsa.dev/spec/v1.2/provenance
- OMG Structured Assurance Case Metamodel: https://www.omg.org/spec/SACM/
- Crossref Crossmark: https://www.crossref.org/services/crossmark/
- DataCite versioning guidance: https://support.datacite.org/docs/versioning
- Cochrane RoB 2: https://methods.cochrane.org/bias/resources/rob-2-revised-cochrane-risk-bias-tool-randomized-trials
- GRADE Working Group: https://www.gradeworkinggroup.org/

## Baseline transition rule

`v0.4` is the historical saturation-planning candidate preserved by this file. Later planning candidates may revise it when one of the following is demonstrated:

```text
A. an existing required capability class is invalid;
B. an invariant is internally inconsistent or contradicted by stronger evidence;
C. a required real-world capability cannot be represented by the existing object/relation/validator/extension model;
D. implementation evidence demonstrates a missing first-class primitive rather than merely a missing module.
```

A new paper, product, benchmark, model, standard, or algorithm that fits an existing extension point is not by itself grounds for `v0.5`.
