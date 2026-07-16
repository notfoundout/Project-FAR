# T-003 Lean Mechanization

## Scope

`mechanization/lean/FARCore.lean` formalizes T-003 as a conditional construction theorem for explicit reasoning processes admitted by a supplied scope predicate.

It does not prove that every mental event or every possible reasoning-like phenomenon is in Project FAR's scope. It proves that, once scope membership and the five stated Project FAR premises are supplied, a six-component FAR representation can be constructed.

## Correspondence with T-003

| T-003 dependency | Lean field | Role |
|---|---|---|
| Axiom 4 — Investigation | `T003Premises.investigation` | Produces `I` for a scoped process. |
| Axiom 1 — Explicit Representation | `representations`, `representationsNonempty` | Produces a nonempty `Rep`. |
| Axiom 2 — Representational Organization | `representationStructure` | Produces `S`, indexed by the selected `Rep`. |
| Axiom 3 — Interpretation | `interpretation` | Produces `Int`, indexed by the selected `I` and `Rep`. |
| Axiom 5 — Reasoning Calculus | `calculus` | Produces `C`. |
| Definition of reasoning trace | `traceOf` | Produces `T` from the process's explicitly specified transition sequence. |

The final witness is `FARRepresentation R = <I, Rep, S, Int, C, T>`.

## What is proved

`FAR.t003_representation_theorem` proves:

```text
for every R,
if R is in the supplied scope,
then FARRepresentation R is nonempty.
```

`FAR.constructFARRepresentation` exposes the constructive witness.

The formalization additionally enforces:

- `Rep` is nonempty;
- `S` is structurally indexed by that exact `Rep`;
- `Int` is indexed by that exact `I` and `Rep`;
- `T` exactly matches the ordered transition signatures explicitly recorded by `R`.

## Assumptions and placeholders

There are no global Lean `axiom` declarations in `FARCore.lean`.

The theorem remains assumption-dependent through `T003Premises`. Those fields are the formal counterparts of A1-A5; Lean checks the construction from them but does not independently prove those premises for all domains.

The following matters remain outside this theorem:

- whether a particular real-world process belongs to the supplied scope;
- whether a concrete representation collection is faithful or information-preserving;
- whether the selected interpretation is semantically correct;
- whether the calculus faithfully captures every admissible transition;
- necessity, minimality, uniqueness, universality beyond the declared scope, or empirical adequacy.

## Proof-object alignment

The mechanization follows `theory/proof-objects/T-003.proof.yaml`:

- steps `s1` through `s5` supply `I`, `Rep`, `S`, `Int`, and `C` from A4, A1, A2, A3, and A5;
- step `s6` permits an empty or specified trace;
- steps `s7` through `s12` assemble the tuple;
- step `s13` generalizes over an arbitrary scoped process.

The Lean theorem compresses the conjunction-introduction steps into construction of one dependent structure, but preserves the same dependency order and claim boundary.

## Validation

```bash
lean mechanization/lean/FARCore.lean
python -m unittest tests.test_t003_lean_alignment
```

CI runs both commands using the pinned toolchain in `lean-toolchain`.
