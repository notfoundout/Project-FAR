# Evidence Authority Model — Research Candidate v1.1

Status: **Research**
Candidacy: **Inactive candidate**
Promotion completed: **No**
Canonical governance implementation: **Deferred**

## Placement and provenance

This file is research evidence produced by `FAR-EVIDENCE-AUTHORITY-MODEL-001`. It is not a canonical governance artifact and has no active authority.

- Question: `research/evidence-authority-model/question-v1.0.md`
- Frozen execution specification: `research/evidence-authority-model/execution-spec-v1.0.json`
- Preregistration commit: `2fe84b72a58e370f814b05a53aa0cf104b17afb1`
- Candidate registry: `research/evidence-authority-model/candidate/registry-v1.0.json`
- Candidate manifest: `research/evidence-authority-model/candidate/proof-artifact-status-manifest-v1.0.json`

Any draft predating preregistration is withdrawn as an unvalidated design sketch. No file may be copied into `docs/governance/`, wired into canonical tests, or treated as active governance until external replication, Acceptance, and Promotion are complete.

## Purpose

This candidate tests a proposition-specific authority contract for Project FAR. It addresses the authority ambiguity identified by `FAR-THEORY-DEPENDENCY-AUDIT-001` without promoting a theory, dependency, proof status, governance rule, or experiment decision.

## Core rule

Under this candidate, an artifact would have authority only when all conditions hold:

1. its authority class is declared;
2. its proposition scope is explicit;
3. its artifact status is permitted for that authority class;
4. an activated, independently promoted registry identifies the scoped owner or owner pattern;
5. required proof, decision, and frozen evidence records are present, resolvable, structurally valid, and linked;
6. no unresolved artifact of equal or higher priority contradicts it for the same proposition, scope, premises, and version; and
7. a unique scoped owner, authorized version, or valid supersession relation is registered.

Existence, repository location, formal notation, repetition, index inclusion, and passing CI do not establish truth or authority.

Artifact status uses only `Accepted`, `Research`, `Provisional`, `Archive`, or `Unknown`. Replication, Acceptance, Promotion, and Repository Change are lifecycle stages, not artifact statuses.

## Authority classes

| Class | May establish after activation | Cannot establish by itself |
|---|---|---|
| `governance_decision` | acceptance, promotion, deprecation, scope, ownership, version, supersession, and change control | theorem or empirical truth |
| `canonical_specification` | definitions, axioms, semantics, interfaces, boundaries, and assumptions within scope | necessity, minimality, universality, or empirical adequacy without separate support |
| `proof_record` | an exact formal result under explicit premises, model class, equivalence relation, and assurance | broader claims outside the registered statement |
| `status_register` | classifications of claims, proofs, dependencies, and statuses | truth of the classified claim |
| `research_record` | frozen observations, counterexamples, executions, and failures within a registered design | canonical theory, Acceptance, Promotion, or global generalization |
| `methodological_specification` | independently adopted procedures | truth of investigated claims or derivability from FARA |
| `index` | discovery and routing | definitions, proof, Acceptance, or observation |
| `historical_record` | provenance and superseded reasoning | active canonical authority |

## Priority and conflict rules

Authority is proposition-specific, not file-wide. **Lower numeric rank means higher authority.** Proposed priority is:

1. scoped governance decision for status and ownership;
2. proof record for its exact statement under its premises;
3. canonical specification for definitions and assumptions within scope;
4. status register for classification only;
5. frozen research record for bounded observation only;
6. methodological specification for adopted procedure only;
7. index and historical records never resolve substantive conflicts.

Therefore priority `1` overrides priority `5` for the same proposition identity when the higher-authority claim is otherwise valid. Recency is not a tiebreaker. If equal-priority artifacts contradict one another for the same proposition, scope, premises, and version, neither proposition is authoritative. The result is `Unknown` until independent governance selects a unique scoped owner/version or records a valid supersession relation. Dual authority for a proposition and its negation is prohibited.

## Governing dependencies

The candidate imports two unresolved governing sources:

- `docs/governance/research-execution-charter.md`, status `Provisional`, supplies the current lifecycle and artifact-status taxonomy;
- `docs/proof-assurance-taxonomy.md`, status `Unknown`, supplies meanings for assurance classifications.

Neither source is upgraded by this campaign. Activation requires each to become `Accepted` through independent governance or be replaced by an independently `Accepted` successor.

## Bootstrap and governance decisions

The bootstrap authority remains `Unknown`. Initial Acceptance or Promotion requires a separate preregistered campaign that identifies and hash-locks an authority predating and independent of this candidate.

`docs/DECISION_LOG.md` is only a proposed future governance-decision owner. It gains no authority from this research candidate.

A decision record used for activation must be resolved from an explicit record store and must contain:

- a stable record identifier;
- an exact decision type and `Accepted` decision status;
- authority class `governance_decision` and `Accepted` governance-authority status;
- an explicit statement that the decision is independent of this candidate;
- exact artifact or manifest identity and version;
- exact status, ownership, or authority-bearing change;
- canonical digest linkage to the decided manifest or artifact bundle;
- a tamper-evident digest over the decision record itself;
- scope, limitations, evidence, date, and superseded decision where applicable.

A missing, unresolvable, self-issued, non-authoritative, mismatched, or hash-invalid decision record supplies no authority.

## Proof authority

The proof inventory must be discovered independently of the proposed owner pattern. Discovery includes:

- theorem metadata `proof` fields;
- lemma metadata `source` fields;
- proposition metadata `source` fields;
- dependency-registry `proof_object` sources;
- every T-001 through T-015 proof object required by `tools/verify_theory.py`;
- structured JSON/YAML fields named `proof`, `proof_object`, `proof_artifact`, `source_proof`, `lean_file`, `proof_registry`, or `entrypoint`;
- fields ending in `_proof_artifact` or `_proof_registry`;
- object-valued registered fields whose nested `path` identifies an artifact;
- self-identifying proof records carrying `proof_id`;
- every syntactically registered Markdown, JSON, YAML, YML, or Lean path, including missing targets so deletion and typo failures remain detectable.

Owner-pattern coverage grants no status or proof authority. A future promoted manifest must:

- have its own independently authoritative, resolvable, hash-valid Acceptance decision;
- identify its exact manifest ID, version, and canonical digest;
- list every registered proof artifact exactly once;
- assign one charter status;
- designate authority-bearing true or false;
- link each status and designation to an independent governance decision record;
- require every entry decision to match the exact manifest, artifact, status, and designation;
- require `Accepted` only for authority-bearing artifacts; and
- exclude all non-authority-bearing artifacts from active proof authority.

A missing target, duplicate entry, missing status, missing designation, missing or invalid decision record, unregistered path, or incomplete discovery pathway blocks activation.

Synthetic activation probes used by this Research campaign are explicitly non-operative. They test the contract but cannot Accept, Promote, populate, or activate the candidate manifest.

## Definition, historical, research, and method boundaries

Canonical names and detailed definitions have separate scopes. Archives can establish provenance only. Research records can establish bounded observations only. Methodological specifications control adopted procedures only. None can silently establish theorem truth, Acceptance, Promotion, or canonical dependency derivation.

## Anti-circularity rules

- No artifact grants itself a higher authority class or status.
- A registry does not prove the claim it classifies.
- A candidate owner is not an active owner.
- A downstream implementation cannot prove an upstream specification necessary.
- CI establishes conformance only.
- The model, registry, manifest, and governance log cannot Accept, Promote, or activate themselves.
- Owner coverage cannot substitute for status.
- Registration cannot substitute for an authority-bearing designation.
- A status register cannot define an assurance taxonomy it merely applies.
- Equal-priority contradiction cannot be resolved by recency, location, or simultaneous authority.
- Numeric priority cannot be reversed: lower rank is always higher authority.
- A decision-record string or file path is not provenance unless the record resolves and passes structural and digest validation.

## Promotion and repository-change gate

Canonical implementation may occur only after a later lifecycle completes:

1. separate preregistration;
2. external independent replication;
3. independent bootstrap selection and hash lock;
4. Acceptance of the exact model, registry, and scope;
5. Promotion of the exact accepted artifacts;
6. resolution or `Unknown` classification of equal-priority conflicts;
7. Acceptance or replacement of governing dependencies;
8. completion and Acceptance of the proof-artifact status manifest;
9. semantic and dependency validation; and
10. an authorized Repository Change that creates canonical governance locations and validation wiring.

Until then, the candidate stays under `research/evidence-authority-model/` and neither authorizes nor prohibits experiments.
