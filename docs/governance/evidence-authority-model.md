# Evidence Authority Model

Status: **Accepted governance specification**

## Purpose

This document defines which Project FAR artifacts may establish canonical propositions, classifications, proof status, methodological requirements, or research observations. It closes the authority ambiguity identified by `FAR-THEORY-DEPENDENCY-AUDIT-001` without promoting any unresolved theory claim.

## Core rule

No artifact is authoritative merely because it exists, is linked from the canonical map, uses formal language, passes repository validation, or is located in a theory or framework directory.

An artifact has authority only when all of the following are true:

1. its authority class is declared;
2. its scope is explicit;
3. its status is permitted for that class;
4. the registry identifies the artifact as the canonical owner of the relevant proposition or classification;
5. any required proof object, decision record, or frozen evidence record is present and linked;
6. no higher-priority authoritative artifact contradicts it.

## Authority classes

| Class | May establish | Cannot establish by itself |
|---|---|---|
| `governance_decision` | acceptance, promotion, deprecation, scope, ownership, and change-control decisions | theorem truth or empirical truth |
| `canonical_specification` | definitions, axioms, semantics, interfaces, framework boundaries, and declared assumptions within stated scope | necessity, sufficiency, minimality, universality, or empirical adequacy unless separately proved or observed |
| `proof_record` | a stated formal result relative to explicit premises, model class, equivalence relation, and proof assurance | broader claims outside the registered statement and premises |
| `status_register` | authoritative classification of claims, proofs, dependencies, and artifact status | the truth of the classified claim |
| `research_record` | frozen observations, executions, counterexamples, and failure reports within the registered design | canonical theory, acceptance, promotion, or global generalization |
| `methodological_specification` | investigation and evaluation procedures adopted by governance | logical derivability from FARA or truth of investigated claims |
| `index` | discovery and routing to canonical owners | definitions, proof, acceptance, or observation |
| `historical_record` | provenance and superseded reasoning | active canonical authority |

## Priority and conflict rules

Authority is proposition-specific, not file-wide. When two artifacts appear to conflict, apply this order:

1. A scoped governance decision controls status and ownership.
2. A registered proof record controls only its exact formal statement under its stated premises.
3. A canonical specification controls definitions and declared assumptions within its scope.
4. A status register controls classification, not underlying truth.
5. A frozen research record controls only what was observed under its registered design.
6. Methodological specifications control adopted procedure, not theory.
7. Indexes and historical records never resolve substantive conflicts.

A later artifact does not automatically outrank an earlier one. Revision requires an authorized change record that names the superseded artifact and the affected proposition.

## Proof authority

Use of `theorem`, `lemma`, `proposition`, `proof`, `derivation`, `necessary`, `sufficient`, `minimal`, `irreducible`, or `universal` requires:

- a unique statement identifier;
- an exact statement;
- declared premises and scope;
- a model class;
- an equivalence or preservation criterion where relevant;
- a proof object or explicit bounded-evidence classification;
- a status entry in `theorem-proof-status-register.md`.

Executable tests may corroborate a proof record or find counterexamples. They do not become proof merely by passing.

## Research authority

A research record is admissible only when its question, design, source identities, execution path, result, and nonclaims are frozen or otherwise provenance-preserved. Research results may update claim status but cannot directly rewrite canonical definitions, axioms, or framework ownership.

## Anti-circularity rules

- An artifact cannot grant itself a higher authority class.
- A registry entry cannot prove the claim it classifies.
- A canonical specification cannot cite its own downstream implementation as proof of necessity.
- A method cannot validate itself solely by satisfying rules it created.
- Passing CI establishes repository conformance only.
- Repetition across multiple files does not increase authority.

## Canonical owners

The machine-readable companion registry is `docs/governance/evidence-authority-registry.json`. It identifies the canonical owner for each authority domain and the evidence required for promotion.

The following existing artifacts retain their stated bounded roles:

- `docs/CANONICAL_MAP.md` is an index, not a source of substantive truth.
- `docs/governance/framework-boundaries.md` owns framework-layer boundaries.
- `docs/governance/theorem-proof-status-register.md` owns theorem/proof classification; linked proof objects remain authoritative for exact statements.
- `docs/governance/claim-status-matrix.md` owns claim-status classification.
- `docs/governance/derivation-status-matrix.md` owns procedure/dependency derivation classification.
- `research/` records evidence and failure reports but does not own canonical theory.

## Promotion gate

A Research or Provisional artifact may become canonical only through a separate governance decision that:

1. names the exact artifact and version;
2. defines the promoted propositions and scope;
3. identifies required proof or evidence;
4. records unresolved counterexamples and limitations;
5. updates the applicable status register and canonical map;
6. passes semantic, dependency, and repository validation;
7. does not claim more than the supporting record establishes.

## Consequence for the next experiment

No experiment may resume on the assumption that FARA, FAR, and FARO dependencies are logically derived until the dependency classification and proof scope are explicitly registered under this authority model. This document establishes authority rules only; it does not settle those dependencies.
