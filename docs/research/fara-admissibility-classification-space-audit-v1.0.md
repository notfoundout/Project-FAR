# FARA admissibility classification-space constraint audit v1.0

Status: **Research result — H5 accepted: no additional normative requirement justified. One genuine canonical defect located. `LIM-028` framing corrected. No canonical surface modified.**
Investigation target: `OP-15` / `UQ-T19`
Kind: deductive authority audit. No experiment, no software, no canonical edit.

Starting position, per the corrected prior result: canonical FARA does **not** fix `Ω` to a three-valued codomain. `Ω` is treated as calculus-parametric. No canonical evidence contradicting that reading was located during this audit; `frameworks/FARA/admissibility-structure.md:84` directly supports it.

## Stage 1 — Authority audit

Surfaces audited in dependency order: `foundations/`; `theory/definitions/definitions.md`, `theory/axioms/axioms.md`, `theory/theorems/propositions.md`; `frameworks/FARA/*.md` (excluding `research/`); `docs/glossary/canonical-terminology.md`; `docs/glossary/canonical-vocabulary-index.md`; `docs/governance/framework-boundaries.md`.

### A — Explicit canonical requirements located

| Source | Requirement | Covers classification-space discrimination? |
|---|---|---|
| `frameworks/FARA/design-principles.md:49` (Principle 3) | "FARA must preserve the distinctions among" transformation rule/execution/result and resolution rule/execution/resolution | **No.** Enumerated *architectural category* separation, not classification values. |
| `frameworks/FARA/architecture.md:191-192` | admissibility ≠ admissibility classification ≠ `Ω` | **No.** Category separation. |
| `frameworks/FARA/admissibility-structure.md:111` (Explicitness) | every candidate has an explicit classification **or** an explicitly represented unresolved status | **No.** Mandates *totality of coverage*, not *discrimination*. |
| `frameworks/FARA/admissibility-structure.md:117-122` (Traceability) | each classification traceable to candidate, investigation, calculus, and reasoning trace | **No.** Provenance, not granularity. |
| `frameworks/FARA/admissibility-structure.md:142-146` (Auditability) | `Ω` should permit reconstruction of **why** each candidate received its classification, via explicit links to classifications, traces, criteria, and representations | **Partially — see B.** |
| `frameworks/FARA/formal-kernel.md:117` | kernel-equivalence preserves **and reflects** every declared relation | **No.** Scoped to model equivalence, not to classification spaces. |
| `frameworks/FARA/admissibility-structure.md:84` | "The admissibility classifications **available** within `Ω` are determined entirely by the applicable reasoning calculus" | **Anti-requirement.** Explicit delegation of the classification space to the calculus. |

### A — Explicit canonical *permissions* that bear directly

Three canonical texts converge on a deliberately permissive stance:

- `theory/definitions/definitions.md:344`: "Representation mappings **may preserve, modify, or discard** structural or semantic properties depending upon their specification."
- `theory/definitions/definitions.md:378`: "**No representation is assumed to possess complete fidelity unless explicitly demonstrated.**"
- `frameworks/FARA/admissibility-structure.md:84`: classification space is calculus-determined.

Shared theory **defines** fidelity (`definitions.md:368`) as a relative, demonstrable quantity. It does not require it. Fidelity is a claim to be proved, not a default property.

### B — Derivable but unstated

1. **Package-level reconstructability.** Auditability plus Traceability derivably require that the *package* — `Ω` together with its criteria and trace links — permit reconstruction of the ground of each classification. They do **not** derivably require that ground to be recoverable from `Ω`'s classification **values**. A calculus may therefore use a coarse classification space while the distinction survives in the criteria links. Status: **Provisional**, resting on a reading of "why".
2. **Layer separation of `unresolved` from `uncertainty`.** `docs/glossary/canonical-terminology.md:36` assigns **uncertainty** ("explicitly recorded lack of warranted determination") to **FARO** as an operational output; `:37` assigns **incompleteness** to FARO. `admissibility-structure.md:111` uses **unresolved status** at the FARA layer. Under `docs/governance/framework-boundaries.md`, a downstream layer must not redefine an upstream concept, so conflating them crosses a layer boundary. Status: **Provisional** — and weakened by finding D2 below.

### C — Located only in evaluation methodology

`FAITHFUL-REP-001` §5.2 (distinction preservation) and §5.3 (preservation **and** reflection) carry the actual obligation. They are methodology, downstream of FARA, and they bind **conditionally on a faithfulness claim being made**.

### D — No located requirement

1. **No canonical requirement that `Ω`'s classification space discriminate calculus-material differences.** Bounded negative search over the surfaces named at the head of Stage 1. Not a proof of absence.
2. **`unresolved status` is normatively used and canonically undefined.** It appears with normative force at `admissibility-structure.md:111`, but is not defined in `theory/definitions/definitions.md`, not listed in `docs/glossary/canonical-terminology.md` — which claims to own "names, meanings, framework ownership, and epistemic class" — and not indexed in `docs/glossary/canonical-vocabulary-index.md`. Bounded negative search over exactly the three surfaces that would own it.

Note: the Charter's artifact status `Unknown` is a different concept at a different layer, and no canonical text links the two. They must not be conflated.

### E — FARA canonically treats this area as open

`frameworks/FARA/admissibility-structure.md:198-208` lists under **Research Status**: "admissibility equivalence; admissibility preservation across transformations; completeness of admissibility classification; minimality of admissibility representation". Canonical FARA therefore classifies these obligations as **open research**, not as settled requirements.

## Stage 2 — Necessity: collapse tests

A distinction is material only where the source or calculus semantics assigns different consequences or interpretations. Each collapse below is tested only under that condition.

| # | Collapse | Violates canonical FARA? | Violates shared theory? | Violates `FAITHFUL-REP-001`? | Verdict |
|---|---|---|---|---|---|
| 1 | tie vs incomparability | No. `:84` grants the calculus its classification space; Explicitness, Traceability, and Auditability are all satisfiable with the distinction carried in criteria links. | No. `definitions.md:344` expressly permits discarding. | Yes, §5.2/§5.3, when a faithfulness claim is made. | **Only methodology (C).** Minimal countermodel `CM-G1` from the prior investigation applies unchanged. |
| 2 | uncertainty vs unresolved | Arguably, via layer separation — but the FARA side of that separation is an undefined term (D2), so the claim rests on undefined ground. | No. | Yes, when material. | **Provisional (B), aggravated by D2.** The only collapse with any canonical traction. |
| 3 | admissible vs degree/rank | No. A calculus is entitled to declare a coarse classification space under `:84`. | No. | Yes, when degrees are material under §2.1 ("or with what weight"). | **Only methodology (C).** |
| 4 | source-distinct classifications generally | No. | No. | Yes, §5.2. | **Only methodology (C).** |

**Necessity result.** No collapse establishes the need for a new canonical requirement. Three of four violate nothing canonical, and the fourth turns on a term canonical FARA has not defined.

## Stage 3 — Architectural placement

| Hypothesis | Disposition | Ground |
|---|---|---|
| **H1** — existing shared-theory requirements already imply everything needed | **Rejected** | Shared theory supplies a *definition* of fidelity and a *permission* to discard, not requirements. There is nothing to imply from. |
| **H2** — a general faithfulness obligation is missing upstream and belongs in shared theory | **Rejected** | It would contradict `definitions.md:344`, which expressly permits mappings to discard, and invert the default at `:378`. A downstream need is not a derivation. |
| **H3** — an admissibility-specific preservation obligation belongs in FARA | **Rejected** | `admissibility-structure.md:204` lists admissibility preservation across transformations as **open research**. Stating it as a requirement would promote research to canonical requirement, violating epistemic discipline. |
| **H4** — FARA imposes an abstract preservation contract; each calculus declares its concrete classification space | **Substantially already the case; the residue is unjustified** | `:84` already delegates the classification space to the calculus. The abstract contract already exists at the methodology layer in `FAITHFUL-REP-001`, conditional on a faithfulness claim. Adding a second contract inside FARA would duplicate it and create a second canonical home for one concept. |
| **H5** — no additional normative requirement is justified | **Accepted** | The permissive architecture is deliberate and triply attested. Faithfulness is a demonstrable claim, not a default obligation. |

No hybrid is constructed: H4's delegation half is already canonical, and its contract half is already methodological. Manufacturing a compromise would add a requirement neither half needs.

## Stage 4 — Derivation and the weakest sufficient rule

Candidate rule, stated as a general invariant with no enumeration:

> **(R)** Where a faithfulness claim is made for `Ω` with respect to a source, `Ω`'s classification space must assign different classifications to any two admissibility conditions to which the applicable calculus assigns materially different consequences or interpretations.

**Classification: derivable — and already stated.** (R) is exactly `FAITHFUL-REP-001` §5.2 distinction preservation, specialized to the admissibility axis. It requires no new canonical text and introduces no independent methodological choice.

Tested against the six required cases:

| Source class | (R) behaviour |
|---|---|
| binary admissibility | Trivially satisfied; no material distinction beyond two classes. |
| extension-valued admissibility | Satisfied by label-set-valued status; distinct memberships get distinct values. |
| gradual / numeric | Satisfied by numeric status; distinct material degrees get distinct values. |
| total ranking | Satisfied by positional status; ties share a position. |
| partial ranking with incomparability | Forces a partially ordered status. `CM-G1` shows a totally ordered status fails. |
| genuine unresolved states | Out of (R)'s scope: `:111` places unresolved status outside the classification and mandates it separately. |

**Counterexamples attempted against (R).**

- *Over-requirement:* does (R) forbid deliberate abstraction or coarsening? No — it is conditional on a faithfulness claim. Absent such a claim, coarsening is permitted by `definitions.md:344`. Attack fails.
- *Under-requirement:* (R) forbids collapse but not *spurious* distinction. A target could invent classifications with no source counterpart. This is real, and is why (R) is only the §5.2 half; §5.3 reflection supplies the other half. Recorded: **(R) alone is insufficient for faithfulness and must not be cited as if it were.**
- *Circularity:* (R) quantifies over "materially different", defined by the calculus's own consequences. If the calculus is the sole judge of materiality, (R) is calculus-relative and cannot detect a calculus that declares nothing material. Attack **succeeds as a scope limit**: (R) cannot police a calculus that declares its own semantics trivial. `FAITHFUL-REP-001` §2.2 handles this externally, requiring a materiality-exclusion certificate challengeable by countermodel. (R) inherits that limit.

**Weakest sufficient rule: none new.** The existing methodological obligation suffices; the correct action is clarification, not addition.

## Stage 5 — Scope control

| Surface | Effect |
|---|---|
| `Ω`'s type | **None.** |
| `Ω`'s semantics | **None.** Clarification only; no meaning changes. |
| FARA primitives | **None.** |
| seven-primitive completeness | **No evidence in either direction.** Representational adequacy is not primitive completeness, and none was inferred. |
| `UQ-T2` / `OP-02` | **Unaffected.** No necessity, minimality, or independence result is touched. |
| terminal UPP theorem | **Unaffected.** Its `E*` admissibility premise is independently frozen and is not the FARA `Ω` architecture. |

No universality is inferred from the accommodation of these source classes. Four source classes accommodated is four source classes accommodated.

## Correction to `LIM-028`

`LIM-028` recorded, from the previous investigation, that no canonical requirement keeps ties, incomparability, uncertainty, and unresolved mutually distinct, and framed this as a **defect**.

The negative search result stands and is reconfirmed here. **The framing was wrong.** The absence is a deliberate architectural delegation, triply attested by `definitions.md:344`, `definitions.md:378`, and `admissibility-structure.md:84`, and explicitly held open by `admissibility-structure.md:204`. It is not a gap.

The genuine defect is narrower and better evidenced: **`unresolved status` carries normative force in canonical FARA and has no canonical definition or terminology-authority owner** (finding D2).

## Proposed minimal revision — not applied

Should authorization and the remaining lifecycle stages be supplied, the smallest sufficient change is a single terminology-authority entry defining `unresolved status`, owned by FARA, classed as a derived status, with canonical detail pointing at `frameworks/FARA/admissibility-structure.md`, and explicitly distinguished from FARO `uncertainty` and from the Charter's artifact status `Unknown`.

**No canonical surface is modified by this investigation.** The Charter lifecycle requires Question → Execution → Observation → Discovery → **Replication** → **Acceptance** → **Promotion** before a repository change to canonical text. Replication and Acceptance have not occurred. The Quality Gate does not establish that a canonical edit is justified on current evidence.

## Nonclaims

This investigation does not establish: that no canonical requirement exists anywhere in the repository, only that none was located on the named surfaces; that the permissive architecture is correct, only that it is deliberate; any primitive necessity, minimality, independence, sufficiency, or completeness result; universality; that `(R)` is complete for faithfulness. No frozen evidence, evaluation record, canonical definition, or software was modified.
