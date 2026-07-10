# Natural Deduction Validation

## Test Case

Target theorem:

`P → (Q → P)`

Representative proof:

1. Assume `P`.
2. Assume `Q`.
3. Reiterate `P`.
4. Discharge the assumption `Q`, deriving `Q → P`.
5. Discharge the assumption `P`, deriving `P → (Q → P)`.

## FAR Mapping

| FAR role | Target-system counterpart |
| --- | --- |
| Investigation | Construct a natural-deduction proof of the target formula. |
| Representation | Formula occurrences, assumptions, subproof markers, and derived conclusions. |
| Representational structure | Nested subproof structure and assumption scope. |
| Interpretation | Optional semantic assignment when soundness or validity is evaluated. |
| Reasoning calculus | Natural-deduction introduction, elimination, reiteration, and discharge rules. |
| Operation | Opening a subproof, reiterating a formula, or discharging an assumption. |
| Reasoning state | Active assumptions plus available formulas at a proof stage. |
| Transition | A rule-licensed change in the proof state. |
| Reasoning trace | The ordered proof with nested scope relations. |
| Resolution | Completion of a derivation of the target theorem. |

## Structural Test

Natural deduction strongly pressure-tests representational structure. A flat list of lines does not preserve which assumptions are active, where subproofs begin or end, or which rules may discharge which assumptions. Scope relations are mathematically relevant.

The same formula token `P` can occur under different active assumptions and therefore occupy different proof roles. FAR's distinction between representation tokens, their structural relations, and reasoning states accommodates this.

## Pressure Findings

1. Proof state is not reducible to the set of formulas present; active-assumption scope matters.
2. Discharge is not ordinary deletion. It is a calculus-licensed operation producing a conditional conclusion and changing dependency structure.
3. A reasoning trace must preserve nested structure, not merely chronological ordering.
4. Interpretation can remain unspecified during syntactic derivation, but is required for a semantic soundness claim.

## Counterexample Search

No explicit natural-deduction proof was found that could dispense with structured representations, scoped investigation, or calculus-relative admissibility. A flat trace would be insufficient, but FAR does not require traces to be flat.

## Result

**PASS**

Foundation v1.0 covers the tested natural-deduction structure without revision. The test also supports the importance of distinguishing proof-state structure from a mere sequence of formula strings.
