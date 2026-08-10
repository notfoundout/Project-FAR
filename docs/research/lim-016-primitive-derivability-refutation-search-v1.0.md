# LIM-016 primitive-derivability refutation search v1.0

Status: **Research result — NULL. No admissible derivation witness found in the tested formalization families. A general obstruction is identified, and `LIM-016` is shown to be self-blocking. No canonical surface modified.**
Investigation target: `LIM-016`
Kind: deductive, strictly one-directional refutation search. No experiment, no software.

**Directionality, stated before results.** A surviving witness could refute a universal independence claim. **Failure to find one establishes nothing** — not independence, not irreducibility, not minimality, not completeness, and not the absence of a fourth or fifth primitive.

## 1. Canonical semantic role of each primitive

| Primitive | Canonical source and text | Functional role | Unformalized terms in the definiens | Testable under `LIM-016`? |
|---|---|---|---|---|
| **Object** | `definitions.md:54` — "anything that is explicitly distinguishable"; no ontological commitment | carrier of identity/distinguishability | *distinguishable* | **Testable** — role determinate even though the term is unformalized |
| **Property** | `definitions.md:62` — "a characteristic that an object may possess"; "may themselves become objects of investigation when explicitly represented" | unary attribution to an object | *characteristic*, *possess*, *may* | **Non-testable** — see §5.2 |
| **Relation** | `definitions.md:70` — "an explicitly specified association **between two or more objects**"; may be represented as objects | n-ary (n ≥ 2) association | *association* | **Testable** — arity is canonically fixed |
| **Representation** | `definitions.md:264ff` — an explicitly distinguishable item used to denote, describe, encode, or refer under an interpretation | denoting item | *used*, *denote* | **Non-testable** at primitive layer; testable only at kernel scope |
| **Interpretation** | `definitions.md:296ff` — assigns meaning to representations | meaning-assigning mapping | *meaning*, *assignment*, *equality of meaning* | **Non-testable** |
| **Investigation** | `definitions.md:414` — "an explicitly specified reasoning objective together with the conditions under which that objective is pursued" | scoping context | *objective*, *conditions*, the *together-with* constructor | **Non-testable** |
| **Reasoning Calculus** | `definitions.md:475` — "a specification of the rules governing admissible reasoning within an investigation" | supplies admissibility criteria and transformation rules | *rule*, *admissibility*, *criterion*, *procedure* | **Non-testable** — and demonstrably so: `ADR-002` is an *open decision* about one of its sub-concepts |

Primitives were not strengthened, weakened, or redefined. Where the canonical semantics are underdetermined, the primitive is marked **non-testable** rather than assigned a preferred meaning, per the Stage 1 rule.

## 2. Derivability criterion, fixed before search

`P_i` is derivable from the remaining six iff there is a construction `D` such that: (1) `D` uses only the remaining primitives plus independently justified background machinery; (2) `D` reproduces `P_i`'s material semantic role; (3) `P_i` behavior is recoverable from `D`; (4) no primitive-equivalent structure is hidden in definitions, auxiliary relations, types, state spaces, constraints, semantics, encodings, or oracle assumptions; (5) removing explicit `P_i` causes no material expressive or operational loss at the tested scope.

Relations kept distinct: lexical definability < representability < simulation < reconstruction < semantic derivability < operational derivability. **Only semantic or operational derivability may support a refutation.** Renaming and re-encoding do not count.

## 3. Formalization-admissibility criterion, fixed before any derivation

A candidate formalization is admissible iff it preserves the canonical primitive distinctions relevant to the test, preserves relevant relations and behaviours, introduces no target-specific assumption whose only purpose is to eliminate a primitive, makes all background structure explicit, separates mathematical convenience from theory commitment, and permits recovery of the canonical primitive interpretation. Auxiliary structures are classified **A** logically/mathematically required · **B** independently motivated by the source semantics · **C** optional representational machinery · **D** target-specific. **Class D cannot establish derivability.**

## 4. Formalization families tested

Two materially different families, each independently defensible, neither invented to force an outcome.

- **F1 — many-sorted relational.** Disjoint sorts per primitive, typed relation symbols, equivalence by sort-preserving isomorphism. Independently defensible: it is the shape of the Accepted kernel and of classical many-sorted model theory.
- **F2 — single-sorted with typed predicates.** One universe, unary predicates marking kinds, relations over the universe. Independently defensible: it is the standard first-order setting, and it is the family in which sortal distinctions become *definable* rather than stipulated — the family most favourable to finding a witness.

F2 was included **specifically because it is the family most likely to yield a refutation**, so that a null result is not an artifact of a conservative modelling choice.

## 5. Derivation attempts

### 5.1 Object

Attempted: Object as position-in-a-relation (structuralist), Object as quotient of indiscernibles. **Both fail.** Every remaining primitive presupposes distinguishable relata — Relation is *between objects*, Property is *of an object*, Representation *denotes objects*. Any construction must already have distinguishable items to relate. **Circular. No witness.**

### 5.2 Property — the strongest candidate, and why it fails

The most promising construction, and canonically licensed: `definitions.md:64` states properties "may themselves become objects of investigation when explicitly represented."

`D_PROP`: reify each property as an Object `p`, and define attribution as a designated binary relation, `Property(o, p) := possesses(o, p)`, with both arguments Objects. Uses only Object + Relation. Canonical arity is respected — `possesses` is binary, so it is a genuine Relation under `definitions.md:70`. Background machinery: one designated relation symbol, class **B**.

Recovery succeeds; property extensions are reconstructible; property-objects are identifiable as the second-argument range of `possesses`.

**It fails the Stage 6 hidden-primitive audit, and the failure is not repairable.** The semantic content of *characteristic* is not reconstructed by the relational structure — nothing structural distinguishes `possesses(o,p)` from any other binary relation such as `adjacent(o,p)`. The content is carried by the **relation symbol's name**, which is relocation into an auxiliary relation, explicitly barred by criterion (4).

The counter-objection is real and was weighed: if using *any* designated relation counted as smuggling, the Relation primitive could never define anything and the criterion would be vacuous. Resolving that requires knowing whether *characteristic* is semantically load-bearing beyond *associated-with*. **Canonical text does not determine this.** Per the Stage 1 rule, Property is therefore marked **non-testable**, not "derivable" and not "independent."

### 5.3 Relation

`D_REL`: `Relation(o₁,…,oₙ) := Property(⟨o₁,…,oₙ⟩)` with a tupling operation. Tupling is arguably class **A**.

**Rejected as relocation.** A tuple *is* an ordered association of objects, which is what Relation canonically denotes. The tupling constructor encodes the association being eliminated. Criterion (4) violated. **No witness.** This is the one clean, decidable rejection in the investigation.

### 5.4 Representation

At primitive-layer scope: **non-testable** — *used* and *denote* are unformalized.

At **kernel scope only**, where `denotes : Representation × Object` has a signature, `D_REPR`: in family F2, `Repr(x) :⟺ ∃y. denotes(x, y)` — Representation as a definable predicate rather than a sort. Recovery succeeds.

**Fails the same audit as `D_PROP`**: denotation-hood is carried by the relation symbol `denotes`, not reconstructed from structure. Additionally, in F1 the construction violates kernel admission constraint 1 (each member in exactly one carrier), so it is not available in that family at all.

### 5.5 Interpretation, Investigation, Reasoning Calculus

All three **non-testable**. Interpretation's definiens rests on *meaning* and *equality of meaning*; Investigation's on *objective*, *conditions*, and an unformalized *together-with* constructor; Reasoning Calculus's on *rule*, *admissibility*, *criterion*, and *procedure* — and `admissibility` is presently the subject of an **open architectural decision** (`ADR-002`), so its semantics are not merely unformalized but formally undecided. No faithful formalization can be assessed for any of the three without selecting a meaning, which Stage 1 forbids.

## 6–8. Hidden-primitive audit, recovery, and the general obstruction

Every construction that survived to the audit stage — `D_PROP`, `D_REPR` — failed in the same way, and the pattern generalizes:

> **General obstruction.** In any relational formalization, eliminating a primitive `P` requires designating a relation symbol whose intended reading carries `P`'s semantic content. The structure alone does not distinguish that symbol from any other relation of the same arity. Whether this constitutes *elimination* or *relocation* depends on whether `P`'s canonical definiens is semantically load-bearing beyond "associated-with" — and canonical FARA does not settle that for any of the seven.

This obstruction is family-independent: it arose identically in F1 and F2, including in F2, which was chosen to be maximally favourable to a witness.

**Consequence — `LIM-016` is self-blocking.** Testing derivability requires formal semantics for the primitives; the absence of exactly those semantics *is* `LIM-016`. The W2/W4/W5 auxiliary-model precedent does **not** transfer: there, auxiliary models supplied *dynamics* while the primitives' meanings were not at issue. Here an auxiliary model would have to supply the primitives' *meanings*, which is the object under test. Doing so would convert a design choice into a discovery — the pattern already rejected in `ADR-002`.

## 9. Null-result control

**No admissible derivation witness was found in the tested formalization families.**

The following are explicitly **not** concluded: that any primitive is independent; that any primitive is irreducible; that the seven primitives are minimal; that they are complete; that no fourth or fifth primitive exists. **The global question remains unresolved.** `W1`'s seven `unresolved` adjudications are unchanged.

## 10. Impact

**No status change to `OP-02`, `OP-03`, `OP-09`, `OP-12`, or `UQ-T2`.** They remain unresolved and remain blocked by `LIM-016`. They are **not** upgraded merely because `LIM-016` was tested — a null result carries no upgrade.

**No propagation** to `OP-01`, the terminal UPP theorem, or any universality claim. No dependency was demonstrated and none is asserted.

**One material change: `LIM-016`'s executability is downgraded.** The preceding prioritization ranked `LIM-016` first on the reasoning that a refutation-seeking formulation avoids the arbitrary-choice trap. **That reasoning is now shown to be wrong.** The refutation direction is blocked by the same missing semantics as the universal direction, because the hidden-primitive audit cannot be discharged without them. This corrects my own prior ranking.

## 11. Preserved negative and non-discriminating evidence

Failed constructions retained: Object-as-relational-position (circular); Object-as-quotient-of-indiscernibles (circular); `D_REL` tupling (relocation — clean rejection); `D_PROP` reification (audit-blocked, non-testable); `D_REPR` definable-predicate (audit-blocked in F2, constraint-violating in F1). The canonical licence at `definitions.md:64` for property reification is recorded as **non-discriminating**: it permits the construction but does not settle whether the construction eliminates or relocates.

## 12. Nonclaims

This investigation does not establish independence, irreducibility, minimality, completeness, or the non-existence of further primitives; does not establish that no witness exists in untested formalization families; does not resolve any primitive's canonical semantics; and does not alter any registered claim. No canonical surface, evaluation record, frozen evidence, or software was modified.
