# T-013 — Relative Soundness Theorem

## Status

Established relative to a supplied target calculus.

---

## Statement

If a FAR representation marks a transition as admissible only when that transition is admissible under the supplied target calculus, then the FAR representation is sound relative to that calculus.

---

## Proof

Let `F` be a FAR representation with reasoning calculus `C`.

Assume the admissibility marking rule for `F` is:

```text
Mark admissible(t) only if C permits t.
```

Let `t` be an arbitrary transition marked admissible in `F`.

By the marking rule, if `t` is marked admissible in `F`, then `C` permits `t`.

Therefore every transition marked admissible in `F` is admissible under `C`.

By definition, a representation is sound relative to `C` when every transition it marks admissible is admissible under `C`.

Therefore `F` is sound relative to `C`.

---

## Corollary

FAR soundness is calculus-relative. FAR does not make a transition valid by labeling it admissible; the label is correct only if the supplied calculus permits it.

---

## Limitation

This proves conditional soundness. It does not prove that any particular supplied calculus is itself truth-preserving, empirically reliable, or normatively correct.
