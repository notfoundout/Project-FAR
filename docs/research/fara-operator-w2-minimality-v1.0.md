# FARA operator W2 bounded minimality result v1.0

Status: **Research result — coordinate-separation-induced bounded minimality; global claim unresolved**  
Proof object: `FARA-OPS-W2-001`

## Authority and scope

The canonical terms are Construct, Differentiate, and Restrict. Canonical prose does not provide transition semantics, observational equivalence, a cost preorder, or an exhaustive operator universe. W2 therefore introduces the explicitly auxiliary model `finite_coordinate_trace_v1` rather than treating its semantics as canonical.

A state is `(R,D,A)`. Construct alone adds to `R`; Differentiate alone adds to `D`; Restrict alone removes from `A`; no operator changes another coordinate. Equality is componentwise and traces are finite and monotone.

## Exact epistemic status

Within that model, all seven proper subsets fail at least one coordinate-isolating witness and the three operators jointly generate every admitted target. This is a valid bounded result, but the minimality is induced by the operator-separating coordinate premise: each operator is made the sole generator of one observable coordinate. It is not independent evidence that the canonical prose denotes a globally necessary or uniquely minimal basis.

The strongest justified claim is therefore:

> Under the operator-separating coordinate premises of `finite_coordinate_trace_v1`, Construct, Differentiate, and Restrict are jointly sufficient and individually irreducible under componentwise equality.

Global sufficiency, global irreducibility, unique basis, canonical operator necessity, and minimality independent of coordinate separation remain unresolved.

## Elimination results

| Operator | Witness | Bounded reason elimination fails |
|---|---|---|
| Construct | `W_C` | Without Construct, `R` is invariant. |
| Differentiate | `W_D` | Without Differentiate, `D` is invariant. |
| Restrict | `W_R` | Without Restrict, `A` cannot decrease. |

## Fourth-operator search

| Candidate | Classification | Boundary |
|---|---|---|
| Resolve | outside scope, unresolved | Canonical Resolve applies a declared rule; the model contains neither rule representation nor rule execution. Restrict plus Construct can only record an already supplied result. |
| Select | outside scope, unresolved | Selection among admissible candidates requires a rule or execution effect absent from the model. |
| Transform | composition in scope | Represent the replacement and restrict the superseded item. |
| Compare | representation convenience | Its modeled output is a recorded distinction. |
| Interpret | outside scope, unresolved | Semantic interpretation is not licensed as a distinction. |
| Observe | outside scope, unresolved | External information acquisition is absent. |
| Delete/relax | outside-scope counterexample | Deleting `R`/`D` or adding to `A` is impossible in the monotone model. |
| Merge | outside scope, unresolved | Quotient or identity-changing effects are unspecified. |

## Remaining obligations

A stronger result requires independently frozen transition semantics, a target system class, an admissible alternative-operator universe, observational equivalence, a cost preorder, rule-execution semantics, and lower bounds that do not assume coordinate locality.

Run `python tools/check_fara_operator_w2.py` and the full repository suite. The validator pins the bounded claim, model identity, nonclaims, obligations, candidate classifications, witnesses, and generated summary.
