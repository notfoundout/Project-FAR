# FARA graded and ranking-based admissibility representation investigation v1.0

Status: **Research result — H1 not eliminated; weakest justified outcome is semantic clarification; canonical `Ω` is not altered**
Investigation target: `OP-14` / `UQ-T18`
Kind: deductive. No experiment, no software added to the repository, no claim depends on execution.

Verification note: every framework, order, and status assignment below is finite and hand-checkable. Two tables were re-derived once by a throwaway enumeration outside the repository purely to check arithmetic. That enumeration is not a repository artifact, is not evidence, and no result depends on it.

## 0. Correction to `docs/research/fara-omega-set-valued-admissibility-v1.0.md`

This investigation located a canonical clause that defeats the central argument of the immediately preceding investigation. The correction is recorded first because it changes a committed result.

**`frameworks/FARA/admissibility-structure.md:84`:** "The admissibility classifications **available** within `Ω` are determined entirely by the applicable reasoning calculus."

Canonical FARA therefore **never fixes the codomain of `Ω`**. `theory/definitions/definitions.md:606` says only that an admissibility classification assigns "admissibility status" to a candidate; no canonical text enumerates the available statuses. `frameworks/FARA/admissibility-structure.md:111` distinguishes a classification from an explicitly represented unresolved status, but does not make the classification binary.

The prior investigation's §4.4 impossibility argument assumed `|Status| = 3` and concluded by pigeonhole that no function `C → Status` could recover an extension family. **That premise is not canonical, so the argument does not hold.** With a calculus-determined status set, the assignment

`Ω(x) = the set of labels of the selected extensions containing x`

is a per-candidate classification, is equivariant under source isomorphism (the induced renaming permutes extension labels along with candidates), and recovers `σ` exactly. Worked for the two frameworks that carried the prior argument:

| Framework | `σ` | `Ω` | `σ` recovered |
|---|---|---|---|
| `𝔉₁` 4-clique mutual | `{{a},{b},{c},{d}}` | `a↦{0}, b↦{1}, c↦{2}, d↦{3}` | exact |
| `𝔉₂` two 2-cycles | `{{a,c},{a,d},{b,c},{b,d}}` | `a↦{0,1}, b↦{2,3}, c↦{0,2}, d↦{1,3}` | exact |

**What survives.** The prior verdict is unchanged in substance: no retyping of `Ω`, no new primitive, and the same unavoidable representational cost. The extension-indexed family `{Ω_E}` and the label-set-valued `Ω` are transposes of one another and carry identical information.

**What is corrected.** The prior investigation classified the repair as a **conservative auxiliary extension**. That over-stated its weight. Because the status codomain was already calculus-parametric, the correct weakest outcome for set-valued admissibility is **semantic clarification**. `CE-ADM-001` is correspondingly weakened: it refutes a *three-valued* `Ω`, not every per-candidate `Ω`.

## 1. Source semantics, fixed before mapping

Two structurally different families are used, per the requirement that graded and ranking-based semantics be distinguished rather than merged.

### 1.1 Ranking-based (ordinal)

Amgoud & Ben-Naim, *Ranking-Based Semantics for Argumentation Frameworks* (SUM 2013). A ranking-based semantics maps an argumentation framework to a **ranking** — a preorder `≽` on arguments, from most to least acceptable. It produces **no extensions and no threshold**. An attack weakens its target rather than eliminating it.

Two sub-cases are kept apart:

- `≽` a **total** preorder: every pair comparable; ties permitted.
- `≽` a **partial** preorder: incomparable pairs permitted.

### 1.2 Gradual (cardinal)

The h-categorizer of Besnard & Hunter, as developed in the gradual-semantics line, assigns each argument a numerical degree in `[0,1]` as the fixed point of

`deg(x) = 1 / (1 + Σ_{y attacks x} deg(y))`.

The output is a **function to a numeric scale**, not merely an order.

### 1.3 Why both are needed

Cardinal output determines ordinal output by forgetting magnitudes; the converse fails. The two families are therefore not interchangeable, and a construction adequate for one is not automatically adequate for the other.

**Not conflated with probability.** Neither semantics is probabilistic. Degrees are not probabilities, are not required to normalise, and carry no event-space or conditioning structure. No probabilistic reading is imported.

## 2. Faithfulness criterion

`FAITHFUL-REP-001` is reused **unchanged**. No requirement was found inapplicable. The specification already anticipates graded content and is directly binding:

- `§2.1` materiality: a fact is material when changing it can change "which transitions are admissible **or with what weight**";
- `§3.2`/`§3.5`/`§3.6` source reducts carry "degree or weight", "probability or weight where present";
- `§6.2`: "graded commitment may not collapse unless the source contract declares them equivalent";
- `§5.4` attribute preservation with `ValEq` fixed before target construction, exact equality the default;
- `§5.3` preservation **and reflection**; `§2.3` axis applicability; `§13` no evaluator-supplied repair.

## 3. Competing hypotheses

- **H1** — canonical `Ω : C → Status` is itself sufficient.
- **H2** — canonical `Ω` unchanged, with auxiliary `G : C → Grade` supplying the additional information.
- **H3** — grade is constitutive of admissibility, so separating it from `Ω` fails faithfulness and `Ω` requires a codomain, type, or semantic change.

H3 is not privileged. H1 was attempted first and to exhaustion.

## 4. H1 constructions attempted

### 4.1 `H1-CARD` — gradual semantics, numeric status

Let the calculus declare `Status = [0,1]`; set `Ω(x) = deg(x)`.

`Ω` remains a per-candidate assignment of a calculus-determined status. Recovery reads `Ω` directly. Distinction preservation and reflection hold because the map is the identity on degrees. `§5.4` is satisfied with exact equality. **H1 succeeds for cardinal semantics.**

### 4.2 `H1-ORD-TOTAL` — total ranking, positional status

Let `Status = ℕ` ordered by rank position; `Ω(x) =` the position of `x` in `≽`. Ties receive equal positions. Recovery reconstructs `≽` from positions. **H1 succeeds for total preorders.**

### 4.3 `H1-ORD-NUMERIC` — partial ranking into a totally ordered status: **rejected**

Countermodel `CM-G1` (`card C = 2`). Two sources over `C = {a,b}`:

- `𝔊_inc`: `≽ = {(a,a),(b,b)}` — `a` and `b` **incomparable**;
- `𝔊_tie`: `≽ = {(a,a),(b,b),(a,b),(b,a)}` — `a` and `b` **tied**.

Any `Ω : C → T` with `T` totally ordered yields `Ω(a) < Ω(b)`, `Ω(a) > Ω(b)`, or `Ω(a) = Ω(b)`. Each asserts a comparative fact. The first two are spurious in both sources; the third represents `𝔊_inc` and `𝔊_tie` identically. Either way `§5.3` reflection fails. **Rejected: a totally ordered status codomain destroys incomparability.**

### 4.4 `H1-ORD-POSET` — partial ranking into a partially ordered status

Let the calculus declare `Status = C/≈` carrying the induced partial order, where `≈` is the symmetric part of `≽`; set `Ω(x) = [x]`.

Then `x ≽ y ⟺ Ω(x) ≥ Ω(y)`, an order embedding, so preservation and reflection both hold. `CM-G1` is separated: in `𝔊_inc` the two classes are incomparable, in `𝔊_tie` they are the single class. **H1 succeeds for partial preorders, provided the status set may carry order structure.**

The order on `Status` is not additional `Ω`-structure. `Ω` is a function into a classification set; the classification set and its structure are calculus content, which `admissibility-structure.md:84` assigns to the calculus. `Ω`'s type, meaning, and per-candidate character are unchanged.

## 5. The `Ω` + `G` separation test

The construction `Ω : C → Status` with a separate `G : C → Grade` was tested directly, holding `Status = {admissible, inadmissible, unresolved}`.

**Case A — the calculus declares a threshold** `Adm(x) ⟺ deg(x) ≥ τ`. Then `Ω` is derivable from `G` and `τ`. The pair is faithful, but `G` carries the admissibility content and `Ω` is a derived projection. `G` is **material, not auxiliary**: by `§2.1`, degree is material whenever it changes admissibility or its weight.

**Case B — no threshold** (the actual Amgoud–Ben-Naim case; ranking semantics produce no extensions). There is no fact of the matter whether `a` is admissible. Two options exist and both defeat H2:

1. record `Ω` as `not_applicable` under `§2.3` — then `Ω` is not representing admissibility at all and `G` is constitutive;
2. force a verdict by supplying a threshold the source does not contain — evaluator-supplied repair, prohibited by `§13`.

**Result: `G` is not merely auxiliary.** Removing grade from the classification destroys preservation and reflection of admissibility itself under threshold-free semantics. **H2 is eliminated as the weakest adequate account.**

This does **not** establish H3, because H1 already succeeds without any change to `Ω`: the grade is carried *as* the status rather than beside it.

## 6. The seven distinctions

| Distinction | Carried by | Separated from |
|---|---|---|
| ordinal information | order relation on `Status` | magnitudes, which it omits |
| cardinal information | numeric `Status` values | order alone, which it refines |
| ties | one shared `Status` element | incomparability |
| incomparability | incomparable `Status` elements | ties and uncertainty |
| uncertainty | interval- or set-valued `Status` element | a precise element |
| unresolved classification | `admissibility-structure.md:111` explicit unresolved status, outside the classification | any classification value, including a least element |
| not applicable | `FAITHFUL-REP-001 §2.3` | unresolved |

**Gap: no requirement located.** Canonical FARA requires that *unresolved* be explicitly represented (`admissibility-structure.md:111`). A search of the canonical terminology authority, the shared definitions, and the FARA architecture, semantics, admissibility-structure, and transition-signature documents **located no requirement** that a calculus keep ties, incomparability, and uncertainty mutually distinct within its classification set. Because the status set is calculus-determined, the obligation to keep these apart has no located canonical home, so a calculus may conflate them undetected.

This is stated as a **negative search result, not a proof of absence**. The repository is large and the search was confined to the canonical surfaces named above. Status: **Provisional**.

## 7. Equivariance and cardinality: premises no longer valid

The prior investigation's equivariance/cardinality argument is **not generalized here**, because its premises fail.

The argument required a finite status codomain of known size. Once the codomain is calculus-determined and may be infinite (`[0,1]`) or arbitrarily structured (any poset), no pigeonhole is available. Equivariance still constrains the constructor — the induced renaming must act on status values that are themselves source-derived — but it no longer bounds expressiveness.

What equivariance still yields: a status set whose elements are **not** source-derived (fixed canonical labels) is forced constant on sources with transitive automorphism groups. This is exactly why the three-valued reading failed and why a calculus-determined reading does not.

## 8. Conservativity

Formalized as projection, using the existing criterion rather than a new one. Let `π : Status → {admissible, inadmissible, unresolved}` be the calculus-declared coarsening (for `H1-CARD`, thresholding at `τ`; for `H1-ORD-POSET`, the declared acceptance cut where one exists).

For any source whose calculus declares only the three classical statuses, `Status` is already that three-element set, `π` is the identity, and `Ω` is literally unchanged. Every previously valid `Ω` structure retains its exact interpretation. **The account is conservative by construction, not by repair.**

Where no acceptance cut exists, `π` is undefined and the classical projection is `not_applicable` — which is a recorded outcome, not a failure.

## 9. Representational versus primitive insufficiency

The insufficiency demonstrated in `§4.3` and `§5` is **representational**: it concerns which classification set a calculus declares, not which primitives exist.

- Grades and ranks are values of a calculus-declared classification set; `Property` already covers represented characteristics with values.
- The order or interval structure on that set is a `Relation`.
- Nothing in any construction above required an operation, object, or structure that could not be stated with the existing candidate primitives.

**This investigation produces no evidence for an additional primitive.** It equally produces **no evidence for seven-primitive completeness**: no exhaustive search over candidate operations was performed, and the absence of a demonstrated need is not a demonstration of sufficiency. `UQ-T2` and `OP-02` are unaffected.

## 10. Rejected constructions preserved

| Construction | Reason for rejection |
|---|---|
| `H1-ORD-NUMERIC` — partial ranking into a totally ordered status | `CM-G1`: destroys incomparability, or asserts spurious comparability; `§5.3` reflection fails. |
| `H2` with three-valued `Ω` plus auxiliary `G`, threshold-free source | `Ω` has no determinate content; forcing a threshold is evaluator-supplied repair under `§13`. |
| `H2` with three-valued `Ω` plus auxiliary `G`, thresholded source | Not faithfulness-failing, but not weakest: `Ω` is a derived projection of `G`, so the separation carries no information the status set does not already carry. |
| Prior `§4.4` pigeonhole as a general impossibility | Premise `card Status = 3` is not canonical; defeated by `admissibility-structure.md:84`. Retained as a refutation of the three-valued reading only. |
| Reading degrees as probabilities | No source semantics warrants it; no normalisation, event space, or conditioning is present. |

## 11. Weakest justified result

**Semantic clarification.** Not "no change", because a real defect was found: canonical text does not require a calculus's classification set to keep ties, incomparability, uncertainty, and unresolved mutually distinct, and the three-valued reading of `Status` is widespread enough in derived material to have defeated a committed argument in the immediately preceding investigation.

Not a conservative auxiliary extension, not a codomain generalization, and not full retyping, because `admissibility-structure.md:84` already makes the classification set calculus-determined. Nothing in `Ω` requires alteration, and per the standing constraint that canonical `Ω` not be altered unless H1 and H2 are both eliminated — H1 is **not** eliminated — no alteration is proposed.

## 12. Nonclaims

This investigation does not establish: that the seven candidate primitives are complete or sufficient; that `H1-ORD-POSET` or `H1-CARD` is unique or minimal; that FARA predicted graded or ranking-based structure, which it accommodates rather than anticipates; any necessity, minimality, independence, or universality result; coverage of infinite candidate sets, probabilistic semantics, set-valued graded semantics, or nonfinite scales; independent replication. The terminal UPP theorem and its independently frozen `E*` admissibility premise are untouched and unaffected. No frozen evidence, evaluation record, or software was modified.

## 13. Highest-information unresolved question remaining

Whether any canonical FARA surface **requires** a calculus's declared classification set to keep ties, incomparability, uncertainty, and unresolved mutually distinct — and if none does, whether that obligation belongs in shared theory, in FARA, or in the calculus contract. This is the first question in this line whose resolution would change a canonical document rather than only a register, and it is decidable by deductive audit of existing text.
