# Classical Propositional Logic Validation

## Test Case

Premises:

1. `P → Q`
2. `P`

Target conclusion:

3. `Q`

The derivation uses modus ponens.

## FAR Mapping

| FAR role | Target-system counterpart |
| --- | --- |
| Investigation | Determine whether `Q` follows from the premises. |
| Representation | Formula tokens `P → Q`, `P`, and `Q`. |
| Representational structure | The language of propositional formulas, premise set, and derivation order. |
| Interpretation | A valuation assigning truth values to propositional variables, when semantic consequence is evaluated. |
| Reasoning calculus | Classical propositional inference rules, including modus ponens. |
| Operation | Applying modus ponens to the two premises. |
| Reasoning state | The current premise and derived-formula set. |
| Transition | Addition of `Q` as a licensed consequence. |
| Resolution | Derivation of the target conclusion. |

## Structural Test

The proof cannot be described as an explicit derivation without formula representations. Those formulas must be organized into a language and a premise/derivation structure. Modus ponens supplies a calculus-relative admissibility condition for the transition from the initial state to the state containing `Q`.

Semantic interpretation is not required to carry out a purely syntactic derivation, but it is required when the claim changes from derivability to truth-preservation or semantic consequence. FAR's distinction between representation, structure, interpretation, and calculus accommodates this difference.

## Pressure Findings

1. FAR must not collapse syntactic derivation into semantic truth. The frozen definitions preserve this separation.
2. A reasoning state may be represented by a set or sequence of formulas, but the state is not identical to any particular serialization of that set.
3. Modus ponens is a rule specification; its application is an operation-token or execution event.

## Counterexample Search

No case of explicit propositional derivation without representations, structure, or a calculus was found. No contradiction arose from mapping the derivation into FAR.

## Result

**PASS**

Classical propositional logic is structurally representable under Foundation v1.0 for the tested derivation. This does not establish that FAR proves propositional logic sound or complete.
