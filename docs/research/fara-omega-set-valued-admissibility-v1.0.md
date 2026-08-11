# FARA `Ω` set-valued admissibility representation investigation v1.0

Status: **Research result — SUPERSEDED IN PART. The `§4.4` general impossibility argument is WITHDRAWN; the `§5` repair is reclassified from conservative extension to semantic clarification. The current adjudication of `OP-13`/`UQ-T15` is `docs/research/fara-graded-admissibility-representation-v1.0.md` §0. Retained in full as research history; encoding-specific results in `§4.1`–`§4.3` survive unchanged.**
Investigation target: `OP-13` / `UQ-T15`
Kind: deductive. No experiment, no software added to the repository, no claim depends on execution.

Verification note: every extension family, automorphism group, and status assignment recorded below is finite and hand-checkable. They were additionally re-derived once by a throwaway enumeration outside the repository, purely to check the author's arithmetic. That enumeration is not a repository artifact, is not evidence, and no result here depends on it. Any reader can confirm the tables by hand.

## 0. Supersession notice (recorded 2026-08-10)

This record is preserved complete as research history. It must not be cited as the current adjudication of `OP-13`/`UQ-T15`.

**Withdrawn.**

- The `§4.4` argument rejecting **every** function `C → Status`. Its premise `|Status| = 3` is **not canonical**: `frameworks/FARA/admissibility-structure.md:84` assigns the available admissibility classifications entirely to the applicable reasoning calculus, so canonical FARA never fixes `Ω`'s codomain. The equivariance/pigeonhole step is sound *given* a three-valued codomain and unsound without it.
- The consequent claim in `§8` that `CE-ADM-001` is **strengthened** to a deductive impossibility for the whole function class.
- The `§7` classification of "every `C → Status` function" as lossy.

**Reclassified.**

- The `§5` repair was recorded as a **conservative extension**. Because the status codomain was already calculus-parametric, no extension was required. The correct weakest outcome is **semantic clarification**. The extension-indexed family `{Ω_E}` and a label-set-valued `Ω` are transposes carrying identical information.

**Surviving unchanged.**

- `§4.1`–`§4.3`: the `E-CRED`, `E-SKEP`, and `E-TRI` encodings each admit explicit finite collisions (`CM-01`–`CM-03`). These are **encoding-specific** refutations and remain valid.
- The substantive verdict: no retyping of `Ω`, no new primitive, and the same unavoidable representational cost, which can be exponential in the candidate count.
- Every nonclaim in `§9`.

**Current adjudication.** `docs/research/fara-graded-admissibility-representation-v1.0.md` §0, which supplies the label-set-valued construction `Ω(x) = the set of labels of the selected extensions containing x`, verified equivariant and exactly recovering `σ` on the two frameworks that carried the withdrawn argument. `CE-ADM-001` refutes the **three-valued** reading of `Ω`, not every per-candidate `Ω`; see `docs/governance/counterexample-register.md`.

## 1. Formal problem statement

### 1.1 Faithfulness criterion — reused, not invented

Faithfulness is taken from the existing canonical mechanism `FAITHFUL-REP-001` (`docs/research/faithful-representation-specification-v1.0.md`). No new faithfulness notion is introduced. The clauses that carry this investigation are:

- **§4 admissible recovery** — recovery receives the target package only, is deterministic, terminating, and uses no hidden oracle;
- **§5.2 distinction preservation** — materially distinct source items receive distinct images;
- **§5.3 relation preservation *and reflection*** — the forward direction prohibits loss, the reverse prohibits spurious material relations;
- **§10.6 uniformity/equivariance** — isomorphic source presentations produce isomorphic target packages under the induced renaming;
- **§12 ledger completeness** — "Metadata is not free: when it carries a material distinction, it is part of the target representation and must be preserved, interpreted, and counted";
- **§13 nontriviality** — no evaluator-supplied repair, no unlinked auxiliary content discharging an obligation.

The applicable source axis is `S_5` (`§3.5`), the admissibility-and-dynamics reduct, which already requires "the distinction between permitted, forbidden, defeated, superseded, and unresolved continuations."

### 1.2 Objects

A **set-valued admissibility semantics** is a pair `𝔄 = ⟨C, σ⟩` where `C` is a finite candidate set and `σ ⊆ 𝒫(C)` is the family of selected admissible sets. `σ = ∅` (no admissible set exists) is permitted and is distinct from `σ = {∅}` (exactly one admissible set, the empty one).

Canonical FARA supplies `Ω : C → Status` (`theory/definitions/definitions.md:614`).

**Correction (2026-08-10).** This section originally read `Status = {admissible, inadmissible, unresolved}`, citing `theory/definitions/definitions.md:606,614` and `frameworks/FARA/admissibility-structure.md:111`. That was a **misattribution**: `definitions.md:606` says only that an admissibility classification is "the explicit assignment of admissibility status to a candidate" and enumerates nothing, and `:111` distinguishes a classification from an explicitly represented unresolved status without making the classification three-valued. `frameworks/FARA/admissibility-structure.md:84` assigns the available classifications entirely to the applicable reasoning calculus. **Canonical FARA does not fix the codomain of `Ω`.** Everything below that depends on `|Status| = 3` is scoped to a three-valued reading, not to canonical FARA.

**Question.** Does there exist a uniform constructor producing a canonical `Ω` from `𝔄` such that admissible recovery reconstructs `σ`?

## 2. Competing hypotheses

- **H1** — `Ω : C → Status` faithfully represents set-valued admissibility with no information loss.
- **H2** — additional indexing is required, but is introducible as a conservative extension over existing primitives without changing `Ω`'s canonical type or meaning.
- **H3** — faithful representation requires changing `Ω`'s canonical type or semantics.

## 3. Witness class — deliberately not Dung-specific

Set-valued admissibility with zero, one, or many selected sets is a broad phenomenon. Systems surveyed:

| System | Set-valued structure | Zero-case |
|---|---|---|
| Dung abstract argumentation (1995) | preferred, stable, complete extensions | stable extensions may not exist |
| Reiter default logic | extensions of a default theory | a default theory may induce no extension |
| Answer set / stable model semantics | stable models | a program may have no stable model |
| AGM partial meet contraction | remainder sets `K⊥p` with a selection function | — |
| Maximal consistent subsets | MCS families | — |
| Legal reasoning (`theory/evaluation/external-system-investigations/legal-reasoning.md:104`) | "multiple plausible outcomes" | — |

Dung frameworks are used below as concrete witnesses because they are finite, hand-checkable, and predate FAR. The result does not depend on their being privileged: the skeptical/credulous split and the zero/one/many extension trichotomy are common to every row.

In-repository precedent exists and is corroborating rather than novel: `docs/research/fara-w3-common-architecture-v1.0.md:29` already records that "multiple extensions require branching machinery", and `theory/evaluation/fara-w3-common-architecture-v1.0.json:55` already records that "selecting one trace silently loses alternative extensions **unless the full extension set is payload**."

## 4. Representation constructions attempted under H1

H1 was attempted constructively before rejection. Four encodings were built and tested.

### 4.1 `E-CRED` — credulous membership

`Ω(x) = admissible` iff `x ∈ ⋃σ`, else `inadmissible`.

Countermodel `CM-01` (`|C| = 3`): `𝔅₁` with attacks `{(a,b),(b,a)}` and `c` isolated has `σ = {{a,c},{b,c}}`. `𝔅₂` with no attacks has `σ = {{a,b,c}}`. Both give `Ω ≡ admissible`. In `𝔅₁`, `a` and `b` are not jointly admissible; in `𝔅₂` they are. **Rejected.**

### 4.2 `E-SKEP` — skeptical membership

`Ω(x) = admissible` iff `x ∈ ⋂σ`, else `unresolved`.

Countermodel `CM-02` (`|C| = 2`): the two-cycle has `σ = {{a},{b}}`, `⋂σ = ∅`. Both arguments self-attacking has `σ = {∅}`, `⋂σ = ∅`. Both give `Ω ≡ unresolved`, but the first has two nonempty selected sets and the second exactly one empty set. **Rejected.**

### 4.3 `E-TRI` — the strongest H1 candidate: skeptical/credulous trichotomy

`Ω(x) = admissible` if `x ∈ ⋂σ`; `inadmissible` if `x ∉ ⋃σ`; `unresolved` otherwise.

This is the standard three-way acceptance classification and repairs both `CM-01` and `CM-02`.

Countermodel `CM-03` (`|C| = 3`), both frameworks fully worked:

- `𝔈₃` — mutual-attack triangle, `R = {(a,b),(b,a),(b,c),(c,b),(a,c),(c,a)}`. Conflict-free sets: `∅, {a}, {b}, {c}`. Each singleton defends itself against both attackers. `σ = {{a},{b},{c}}`. `⋂σ = ∅`, `⋃σ = {a,b,c}`, so `Ω ≡ unresolved`.
- `𝔈₄` — `R = {(a,b),(b,a),(a,c)}`. Conflict-free sets: `∅, {a}, {b}, {c}, {b,c}`. `{a}` is admissible; `{c}` is not (it cannot counter `a`); `{b,c}` is admissible because `b` counters `a`, the sole attacker of both `b` and `c`. Maximal admissible sets: `{a}` and `{b,c}`. `σ = {{a},{b,c}}`. `⋂σ = ∅`, `⋃σ = {a,b,c}`, so `Ω ≡ unresolved`.

Identical `Ω`; materially different `σ`. In `𝔈₄`, `b` and `c` are jointly admissible; in `𝔈₃` no two candidates are jointly admissible. **Rejected.**

### 4.4 `E-*` — general impossibility, encoding-independent — **WITHDRAWN**

> **WITHDRAWN 2026-08-10.** The argument in this subsection is **unsound as a general result** and must not be cited. It assumes `|Status| = 3`, which `frameworks/FARA/admissibility-structure.md:84` shows is not canonical — the available classifications are determined entirely by the applicable reasoning calculus. Under a calculus-determined status set the pigeonhole does not close, and `Ω(x) =` the set of labels of the selected extensions containing `x` recovers `σ` exactly while remaining equivariant. The subsection is retained verbatim below as research history. It remains valid **only** as a statement about a three-valued codomain. See `docs/research/fara-graded-admissibility-representation-v1.0.md` §0.

The three rejections above are encoding-specific. The following argument rejects **every** function `C → Status`, using only `FAITHFUL-REP-001 §10.6` equivariance and `|Status| = 3`.

If a source presentation has an automorphism group acting transitively on `C`, then equivariance forces the induced `Ω` to be **constant** on `C`. Exactly three constant maps exist.

Four frameworks on `C = {a,b,c,d}`, each with a transitive automorphism group and pairwise distinct `σ`:

| Framework | Attack relation | `σ` (preferred) | Automorphisms |
|---|---|---|---|
| `𝔉₁` | mutual-attack 4-clique | `{{a},{b},{c},{d}}` | `S₄`, transitive |
| `𝔉₂` | two disjoint 2-cycles `a↔b`, `c↔d` | `{{a,c},{a,d},{b,c},{b,d}}` | contains `(ab)`, `(cd)`, `(ac)(bd)`; transitive |
| `𝔉₃` | empty | `{{a,b,c,d}}` | `S₄`, transitive |
| `𝔉₄` | all self-attacking | `{∅}` | `S₄`, transitive |

Four materially distinct sources, all forced to constant `Ω`, three constant values available. By pigeonhole at least two receive the same `Ω`, so no injective uniform constructor exists and admissible recovery of `σ` is impossible.

**`H1` is refuted.** The refutation is deductive, encoding-independent, and does not depend on which multi-extension semantics is chosen.

> **End of withdrawn subsection.** The sentence immediately above is **withdrawn as stated**. What survives is the strictly weaker claim: *`H1` fails for a three-valued codomain.* `H1` is **not** refuted for calculus-determined status sets, and the surviving refutations of `H1` are the encoding-specific collisions `CM-01`–`CM-03` in `§4.1`–`§4.3`.

## 5. H2 construction and conservativity test

### 5.1 Construction

Keep `Ω : C → Status` **exactly as canonically defined**. Represent a set-valued semantics as an extension-indexed family

`{Ω_E}` for `E ∈ σ`, where each `Ω_E` is an ordinary canonical `Ω` recording membership in `E`,

together with an explicit representation of the index family `σ`.

### 5.2 Existing primitives suffice

| Component | FARA construct | Primitive status |
|---|---|---|
| each `E ∈ σ` | a Representation whose members are candidates | existing candidate primitives Representation, Object |
| membership of a candidate in `E` | a Relation | existing candidate primitive Relation |
| each `Ω_E` | a canonical Admissibility Structure, unchanged in type and meaning | existing derived component |
| the indexed family | a Relation between extension representations and admissibility structures | existing candidate primitive Relation |

No new primitive is introduced. This is **additional representational structure, not an additional reasoning primitive.**

Canonical FARA already contemplates more than one `Ω`: "Ω may be associated with one or more reasoning state representations" (`frameworks/FARA/admissibility-structure.md:154`) and "Changes to any of these may produce a different Admissibility Structure" (`:64`). No canonical text asserts that an investigation has exactly one `Ω`.

### 5.3 Conservativity

Where `card σ = 1` the family collapses to a single `Ω_E`, which is the canonical `Ω` with its canonical interpretation. Grounded semantics, which always yields exactly one extension by Knaster–Tarski monotonicity, is unaffected. Every previously valid `Ω` structure retains the same interpretation. **The extension is conservative.**

### 5.4 The four distinctions the plain `Ω` destroyed

| Distinction | Plain `Ω` | H2 family |
|---|---|---|
| multiplicity (many selected sets) | collapses to one status | `card σ ≥ 2` |
| nonexistence (`σ = ∅`) | indistinguishable from `σ = {∅}` | empty index family vs one empty extension |
| uncertainty (candidate unresolved within a fixed extension) | conflated | `Ω_E(x) = unresolved` |
| underdetermination (in some but not all extensions) | conflated with uncertainty | derivable from the family |

All four are preserved and mutually distinguishable.

### 5.5 The apparent order inversion dissolves

`docs/research/fara-admissibility-priority-v1.0.md` F6 recorded that multi-extension selection appeared to force a resolution-like step upstream of `Ω`, inverting FARA's calculus → `Ω` → resolution order. Under H2 the inversion disappears: computing the family `σ` is admissibility-criteria work owned by the calculus (`D1`), and selecting one `E` from `σ` is resolution work operating on the family. The stated order is preserved. The earlier appearance of inversion was an artifact of forcing a single `Ω`.

## 6. Countermodels against H2

| Attack | Result |
|---|---|
| Index family smuggles undeclared machinery | **Fails.** The family is finite for finite sources and is declared and counted under `§12`. |
| Violates `Ω` non-determination (`D5`) | **Fails.** Each `Ω_E` still records rather than determines; the calculus determines `σ`. |
| Unlinked auxiliary content repairing a failed embedding (`§5.5`) | **Fails.** The index family is explicitly linked to each `Ω_E`, not free-floating metadata. |
| Representational cost | **Survives as a cost finding, not an expressive failure.** `card σ` can be exponential in `card C`: `n/2` disjoint 2-cycles yield `2^(n/2)` preferred extensions. H2 is faithful but not polynomially bounded, and the cost is charged under `§12` "cost-bearing helper structures". |
| Target-side surplus distinction | **Survives as a recorded surplus.** `Ω_E`'s `unresolved` value has no counterpart inside a fixed Dung extension, where membership is binary. Permitted under `§5.5` image accountability, but recorded: FAR introduces a distinction with no source counterpart here. |
| Infinite extension families | **Out of scope, Unknown.** Outside Project FAR v1.0 finite explicit auditable scope (`LIM-025`). |
| Graded / ranking-based acceptability | **Not covered by H2.** Degree-valued acceptability would require retyping `Status` itself. This is a distinct phenomenon from set-valued admissibility and is not adjudicated here. |

## 7. Embedding classification

- H1 encodings (`E-CRED`, `E-SKEP`, `E-TRI`): **lossy**. Established by explicit finite collisions; survives.
- ~~and every `C → Status` function~~: **withdrawn** — see `§0` and `§4.4`. A label-set-valued `Ω` under a calculus-determined status set is faithful.
- H2 extension-indexed family: **faithful** at finite scope, with declared and charged cost. Reclassified from conservative extension to **semantic clarification**.

**Prediction versus relabeling.** H2 accommodates extension structure after observing it; it does not predict that multi-extension semantics arise. Per the counterexample discipline against post-hoc mappings, H2 is recorded as **accommodation, not prediction**. A faithful embedding does not show that FARA discovered this structure.

## 8. Impact on existing FARA claims and dependencies

- ~~`CE-ADM-001` is **strengthened** from an expressive-loss observation to a deductive impossibility result for the whole function class `C → Status` (`§4.4`).~~ **WITHDRAWN 2026-08-10.** `CE-ADM-001` stands at its original scope: it refutes the **three-valued** per-candidate reading of `Ω`, not every per-candidate `Ω`. The corrected row is in `docs/governance/counterexample-register.md`.
- `LIM-026` remains open in substance, narrowed to the **three-valued** reading: the boundary is that reading, not per-candidate `Ω` as such, and not FARA's primitives.
- `OP-13` / `UQ-T15` are **resolved at finite scope** in favour of semantic clarification, not conservative extension. H3 is not required for set-valued admissibility. The current adjudication is `docs/research/fara-graded-admissibility-representation-v1.0.md` §0.
- `theory/evaluation/external-systems/argumentation-frameworks.md`'s `conservative extension` classification is **corroborated**, and its justification gap is now closed by an explicit construction rather than by assertion. The record itself is unmodified.
- `docs/research/fara-admissibility-priority-v1.0.md` F6 is **superseded** by `§5.5` above: the apparent order inversion was an artifact.
- The seven candidate primitives are unchanged. No sixth primitive is indicated.
- **No effect on the terminal UPP theorem.** Its `E*` admissibility premise is independently frozen and is not the FARA `Ω` architecture.

## 9. Nonclaims

This investigation does not establish: that FARA predicted or discovered multi-extension structure; that H2 is the unique or minimal faithful construction; any primitive necessity, minimality, independence, or sufficiency result; universality; polynomial representational cost; coverage of infinite extension families, graded acceptability, or nonfinite semantics; independent replication. No frozen evidence, evaluation record, or software was modified.

## 10. Highest-information unresolved question remaining

Whether graded and ranking-based acceptability semantics, whose values are degrees rather than sets, require retyping `Ω`'s `Status` codomain. H2 does not cover that case, and the `§4.4` equivariance argument suggests a finite `Status` set is vulnerable to the same pigeonhole pressure whenever the source admits more equivariance classes than `Status` has values.

**Answered, and it defeated `§4.4` (2026-08-10).** `OP-14`/`UQ-T18` resolved this: retyping is **not** required, because `frameworks/FARA/admissibility-structure.md:84` already makes the status set calculus-determined. That same clause removes the `|Status| = 3` premise on which `§4.4` rested, which is why `§4.4` is withdrawn. Evidence: `docs/research/fara-graded-admissibility-representation-v1.0.md`.
