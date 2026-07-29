# Evidence Authority Model

Status: **Research**
Candidacy: **Inactive candidate**
Promotion completed: **No**

## Research provenance

This version is the candidate output of `FAR-EVIDENCE-AUTHORITY-MODEL-001`.

- Question: `research/evidence-authority-model/question-v1.0.md`
- Frozen execution specification: `research/evidence-authority-model/execution-spec-v1.0.json`
- Preregistration commit: `2fe84b72a58e370f814b05a53aa0cf104b17afb1`

Any draft predating that preregistration is withdrawn as an unvalidated design sketch. Only the post-preregistration candidate, execution record, observation, discovery, and replication record may support this Research artifact. None may Accept or Promote it.

## Purpose

This document proposes which Project FAR artifacts may establish canonical propositions, classifications, proof status, methodological requirements, or bounded research observations. It addresses the authority ambiguity identified by `FAR-THEORY-DEPENDENCY-AUDIT-001` without promoting any unresolved theory or governance claim.

This artifact remains Research until a separately preregistered lifecycle completes external replication, Acceptance, and Promotion. Until then, it is an inactive candidate and cannot authorize its own adoption, any downstream promotion, or any experiment decision.

## Core rule

No artifact is authoritative merely because it exists, is linked from the canonical map, uses formal language, passes repository validation, or is located in a theory or framework directory.

Under this candidate model, an artifact would have authority only when all of the following are true:

1. its authority class is declared;
2. its proposition scope is explicit;
3. its artifact status is permitted for that authority class;
4. the activated registry identifies the artifact or owner pattern for that proposition scope;
5. any required proof object, decision record, or frozen evidence record is present and linked;
6. no unresolved authoritative artifact of equal or higher priority contradicts it for the same proposition, scope, premises, and version;
7. the registry identifies a unique scoped owner or an authorized version/supersession relation for that proposition.

Artifact status uses only the charter taxonomy: `Accepted`, `Research`, `Provisional`, `Archive`, or `Unknown`. Replication, Acceptance, and Promotion are lifecycle stages; Promotion is not an artifact status. `Unknown` and `Provisional` never silently acquire active authority.

## Authority classes

| Class | May establish | Cannot establish by itself |
|---|---|---|
| `governance_decision` | acceptance, promotion, deprecation, scope, ownership, and change-control decisions | theorem truth or empirical truth |
| `canonical_specification` | definitions, axioms, semantics, interfaces, framework boundaries, and declared assumptions within stated scope | necessity, sufficiency, minimality, universality, or empirical adequacy unless separately proved or observed |
| `proof_record` | an exact formal result relative to explicit premises, model class, equivalence relation, and proof assurance | broader claims outside the registered statement and premises |
| `status_register` | classification of claims, proofs, dependencies, and artifact status | the truth of the classified claim |
| `research_record` | frozen observations, executions, counterexamples, and failure reports within the registered design | canonical theory, acceptance, promotion, or global generalization |
| `methodological_specification` | investigation and evaluation procedures adopted by governance | logical derivability from FARA or truth of investigated claims |
| `index` | discovery and routing to canonical owners | definitions, proof, acceptance, or observation |
| `historical_record` | provenance and superseded reasoning | active canonical authority |

## Priority and conflict rules

Authority is proposition-specific, not file-wide. When two activated artifacts conflict, this candidate model proposes the following order:

1. A scoped governance decision controls status and ownership.
2. A registered proof record controls only its exact formal statement under its stated premises.
3. A canonical specification controls definitions and declared assumptions within its scope.
4. A status register controls classification, not underlying truth.
5. A frozen research record controls only what was observed under its registered design.
6. Methodological specifications control adopted procedure, not theory.
7. Indexes and historical records never resolve substantive conflicts.

A later artifact does not automatically outrank an earlier one. Revision requires an authorized change record naming the superseded artifact, version, affected proposition, and scope.

If two equal-priority artifacts contradict one another for the same proposition, scope, premises, and version, neither proposition is authoritative. The result is `Unknown` until an independently authorized governance decision selects a unique scoped owner/version or records a valid supersession relation. Dual authority for a proposition and its negation is prohibited.

## Governing dependencies

The activated map must register every artifact whose rules the model imports.

- `docs/governance/research-execution-charter.md` supplies the current Research lifecycle and five-value artifact-status taxonomy. It is currently `Provisional`, so it cannot govern an activated model until independently transitioned to `Accepted` or replaced by an independently Accepted successor.
- `docs/proof-assurance-taxonomy.md` supplies meanings for proof-assurance classifications. Its charter status is currently `Unknown`, so those meanings cannot carry active canonical authority until independently transitioned to `Accepted`.

The candidate does not upgrade either dependency. Their unresolved transitions block activation.

## Bootstrap and governance decisions

This Research candidate does not grant `docs/DECISION_LOG.md` authority. The registry lists it only as the proposed future owner of governance decisions after activation.

Initial Acceptance or Promotion of this model requires a separate preregistered campaign that selects and hash-locks an Accepted-status or promotion-provenance authority whose authority predates this model. Until that external bootstrap authority is identified and validated, the bootstrap status is `Unknown`, the registry remains inactive, and no decision in `docs/DECISION_LOG.md` can derive authority from this candidate.

The activated authority map must explicitly register this model and its registry as separate `canonical_specification` owners. Both currently remain `Research`; each must receive an independently authorized transition to `Accepted`. The registry entry cannot perform either transition itself.

After valid activation, a governance decision would be authoritative only for the exact decision it records and only when it identifies the decision, date, deciding authority, affected artifact and version, exact status or ownership change, supporting evidence, limitations, and superseded decision where applicable.

## Proof authority

The registry separately assigns theorem/proof classification to `docs/governance/theorem-proof-status-register.md`, assurance-level meanings to `docs/proof-assurance-taxonomy.md`, and exact proof objects to a proof-record owner pattern that includes every proof artifact path registered by repository JSON, YAML, Markdown, verifier-declared, and Lean metadata pathways.

The proof discovery contract independently enumerates:

- theorem `proof` fields;
- lemma `source` fields;
- dependency-registry `proof_object` sources;
- every T-001 through T-015 proof object required by `tools/verify_theory.py`;
- JSON and YAML path fields named `proof_object`, `proof_artifact`, `source_proof`, `lean_file`, or `proof_registry`, plus keys ending in `_proof_artifact` or `_proof_registry`;
- self-identifying JSON proof records carrying a `proof_id`;
- every referenced Markdown, JSON, YAML, and Lean artifact that exists in the repository.

Owner-pattern coverage establishes only proposed ownership. It does not establish artifact status or active proof authority. Before activation, the promotion lifecycle must complete and independently Accept `docs/governance/proof-artifact-status-manifest.json`. That manifest must link its own independent Acceptance decision, list every registered proof artifact exactly once, assign one charter-recognized artifact status, and designate whether the artifact is authority-bearing.

Only proof artifacts designated authority-bearing must have status `Accepted`. Registered proof artifacts intentionally retained as `Research`, `Provisional`, `Archive`, or `Unknown` may remain non-Accepted, but must be explicitly excluded from active proof authority. A missing status, duplicate entry, missing authority-bearing designation, missing manifest-level Acceptance record, or unregistered proof path blocks activation.

Use of `theorem`, `lemma`, `proposition`, `proof`, `derivation`, `necessary`, `sufficient`, `minimal`, `irreducible`, or `universal` requires a unique statement identifier, exact statement, premises, scope, model class, preservation criterion where relevant, linked proof object or bounded-evidence classification, and a status-register entry.

Executable tests may corroborate a proof record or find counterexamples. They do not become proof merely by passing.

## Definition ownership

Canonical terminology and detailed definitions have separate proposition scopes:

- `docs/glossary/canonical-terminology.md` proposes ownership of canonical names and short declared meanings;
- `theory/definitions/definitions.md` proposes ownership of detailed formal definitions.

The detailed-definition artifact currently has status `Unknown` because it has no explicit status declaration. Activation therefore requires a separately governed transition of that artifact to `Accepted`; ownership registration alone does not make it authoritative.

## Historical authority

Artifacts under `archive/**` may serve as `historical_record` sources only while their artifact status is `Archive`. They may establish provenance and superseded reasoning, but never active canonical authority.

## Research authority

A research record is admissible only when its question, design, source identities, execution path, result, and nonclaims are frozen or provenance-preserved. Research status may support bounded observations but cannot directly rewrite canonical definitions, axioms, ownership, Acceptance, or Promotion.

## Anti-circularity rules

- An artifact cannot grant itself a higher authority class.
- A registry entry cannot prove the claim it classifies.
- A candidate owner is not an active owner.
- A canonical specification cannot cite its downstream implementation as proof of necessity.
- A method cannot validate itself solely by satisfying rules it created.
- Passing CI establishes repository conformance only.
- Repetition across files does not increase authority.
- This model and registry cannot Accept, Promote, or activate themselves.
- The initial bootstrap authority must predate and be independent of this model.
- Proof-owner coverage cannot substitute for an explicit permitted artifact status.
- Registration as a proof artifact cannot substitute for an authority-bearing designation.
- The proof-artifact status manifest cannot Accept itself or assign status without linked independent governance decisions.
- A status register cannot define the assurance classes it merely applies unless the taxonomy is separately registered.
- An unresolved equal-priority contradiction cannot be resolved by recency, file location, or simultaneous authority.

## Promotion gate

This Research candidate may become active only through a separately preregistered lifecycle that:

1. selects and hash-locks an independent pre-existing bootstrap authority;
2. names the exact model and registry versions;
3. defines promoted propositions and scope;
4. identifies required proof or evidence;
5. records external replication, Acceptance, and Promotion separately;
6. independently transitions this authority model and its registry to `Accepted`;
7. independently transitions the governing research-execution charter and proof-assurance taxonomy to `Accepted` or identifies independently Accepted successors;
8. transitions every other proposed canonical owner lacking an explicit permitted status through separate governance;
9. independently transitions the proof-artifact status manifest to `Accepted` and links the manifest-level Acceptance decision;
10. completes the manifest with exactly one charter status and one authority-bearing designation per registered proof artifact;
11. requires `Accepted` only for authority-bearing proof artifacts and excludes all others from active proof authority;
12. verifies a unique scoped owner/version or valid supersession relation for every proposition and sends unresolved equal-priority conflicts to `Unknown`;
13. records unresolved counterexamples and limitations;
14. updates the applicable status register and canonical map;
15. passes semantic, dependency, and repository validation;
16. does not claim more than the supporting record establishes.

Until every requirement is satisfied, activation remains prohibited and authority conclusions remain `Unknown`.

## Proposed consequence after promotion

If this model is later Accepted, Promoted, and activated through the required independent lifecycle, it would prohibit resuming an experiment on the assumption that FARA, FAR, and FARO dependencies are logically derived until dependency classification and proof scope are explicitly registered. This Research candidate itself neither authorizes nor prohibits the next experiment.
