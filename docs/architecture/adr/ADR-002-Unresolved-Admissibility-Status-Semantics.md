# ADR-002

## Title

Semantics of FARA `unresolved status`

## Status

Open — decision required. **No alternative is selected.**

This ADR does not record a decision taken. It records a decision that must be taken, because four completed investigations established that the question is not answerable from evidence.

## Date

2026-08-10

## Context

`frameworks/FARA/admissibility-structure.md:111` states:

> "Every candidate admitted for consideration should possess either an explicit admissibility classification or an explicitly represented unresolved status."

This is the **only** occurrence of `unresolved status` in canonical FARA, and the only technical occurrence of `status` in canonical FARA that has neither a governing definition nor a stated categorization.

Four investigations, `OP-15` through `OP-18`, converged on this clause from different directions and are now closed as **evidence-exhausted**:

| Investigation | Result bearing on this clause |
|---|---|
| `OP-15` — classification-space constraints | No canonical requirement governs classification-space granularity. The permissive stance is deliberate: `theory/definitions/definitions.md:344` permits mappings to discard, `:378` makes fidelity a demonstrable claim rather than a default, and `admissibility-structure.md:84` delegates the classification space to the calculus. |
| `OP-16` — what `unresolved status` is | Owner established as FARA. Typing **weakly** established as a meta-status outside the calculus-determined classification set, resting on a non-redundancy reading of `:111` that is a reading rather than a forced inference. Semantic content returned as underdetermined. |
| `OP-17` — obligation scope | Whether unresolved candidates carry traceability and auditability obligations is **interpretation-relative**: the asymmetry holds under one reading and dissolves under the other, and canonical text supports both. |
| `OP-18` — the term `status` | `status` is univocal under one recoverable definition; the ambiguity lies in the compound construction `N status` and bites at exactly this occurrence. The ambiguity **cannot** be eliminated without a new design choice. |

The question is therefore **not a discoverable fact**. It is an architectural decision that canonical evidence underdetermines.

## Problem Statement

Should FARA `unresolved status` denote:

- **A** — a substantive admissibility classification supplied by the applicable reasoning calculus; or
- **B** — a FARA-level meta-status indicating that no substantive admissibility classification is currently available?

## Alternatives

Both alternatives are recorded with their established consequences. Consequences listed here were derived by the closed investigations and are preserved verbatim in substance; none is offered as an argument for selection.

### Alternative A — substantive admissibility classification

`unresolved` is a value in the calculus-determined classification set `S_K`. "Unresolved status" is then the value-naming form of "admissibility status".

**Established consequences.**

1. `:111` becomes redundant: its second disjunct is subsumed by the first, since `admissibility-structure.md:23` defines a classification as the explicit assignment of admissibility status to a candidate. (`OP-16`, `OP-18`)
2. Traceability (`:117`) and Auditability (`:144`) attach automatically, because both are scoped to "admissibility classification". The obligation asymmetry identified in `OP-17` dissolves. (`OP-17`)
3. A tension arises with `admissibility-structure.md:84`, which makes the available classifications determined **entirely** by the calculus: a calculus may declare `S_K` without an unresolved value, leaving `:111` unsatisfiable for candidates it cannot classify. Because `:111` is a "should", this is tension rather than contradiction. (`OP-16`)
4. Traceability would require linking to "the reasoning process or reasoning trace **that produced the classification**". In nontermination and missing-input cases nothing produced a result, so the required producing process may not exist. (`OP-17`)
5. Auditability would require reconstructing why the candidate received the unresolved value. Under an unknown cause this is unsatisfiable, so the obligation survives only in a weak form that adds nothing to `:111`'s existing marker requirement. (`OP-17`)

### Alternative B — FARA-level meta-status

`unresolved` lies outside `S_K`. Formally `Ω_K : C → S_K ∪ {⊥}` with `⊥ ∉ S_K`.

**Established consequences.**

1. `:111` is non-redundant and is satisfiable regardless of which classification set a calculus declares. (`OP-16`)
2. Traceability and Auditability do not attach, because both are scoped to "admissibility classification". Unresolved candidates carry neither obligation, an asymmetry canonical text neither states nor defends. (`OP-17`)
3. `:111` requires a marker only; no reason structure is forced. (`OP-16`)
4. Two candidates may be unresolved for different reasons with no obligation to distinguish them. (`OP-16`)
5. The shape matches the CRP `Unknown` precedent, which is epistemically incomparable with the ordered preservation values — but that precedent is methodology-layer and carries no upstream authority. (`OP-16`)

### Evidence that does **not** discriminate

Recorded so that it is not mistaken for support in either direction.

- Removal of awkwardness, implementation convenience, preferred typing, and cleaner formal treatment are downstream consequences, not lexical authority.
- The failed substitution of "admissibility status" into `:111` restates `OP-16`'s non-redundancy argument; it is one argument, not two.
- FAR `Unresolved` (`frameworks/FAR/workflow.md:136`) is defined, but for a different subject — an investigation closure, not a candidate — and lies downstream, so it cannot supply an upstream definition.
- FARO `uncertainty`, the Charter artifact status `Unknown`, and CRP `Unknown` are distinct concepts at distinct layers and were not merged.

### Not in scope for this decision

Selecting A or B fixes the **structural** question only. It does **not** settle which of insufficient evidence, conflicting criteria, nontermination, missing input, calculus-defined indecision, evaluator failure, or unknown cause the term covers. `OP-16` returned that semantic content as underdetermined, and this ADR does not resolve it.

One derived separation stands under either alternative: a source semantics' explicit "undecided" **value** belongs in `S_K` and is a substantive classification, not unresolved.

## Decision

**None. Deferred pending authorization.**

Selection requires the Charter lifecycle. This ADR supplies the Question, Execution, Observation, and Discovery stages; Replication, Acceptance, and Promotion have not occurred.

## Consequences of not deciding

`OP-16`, `OP-17`, and `OP-18` remain closed as evidence-exhausted rather than resolved. `LIM-029` and `LIM-030` remain open as recorded boundaries. No canonical surface changes, and `Ω`'s type and semantics, the seven candidate primitives, and the terminal UPP theorem are unaffected in either case.

## References

- `frameworks/FARA/admissibility-structure.md`
- `docs/research/fara-admissibility-classification-space-audit-v1.0.md` (`OP-15`)
- `docs/research/fara-unresolved-status-audit-v1.0.md` (`OP-16`)
- `docs/research/fara-unresolved-obligation-scope-audit-v1.0.md` (`OP-17`)
- `docs/research/fara-status-term-audit-v1.0.md` (`OP-18`)
- `docs/governance/limitations-register.md` — `LIM-029`, `LIM-030`
