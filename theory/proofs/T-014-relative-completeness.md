# T-014 — Relative Completeness Theorem

## Status

Established relative to a supplied target calculus and explicit transition domain.

---

## Statement

If a FAR representation includes a transition signature for every transition permitted by the supplied calculus within a specified transition domain, then the representation is complete relative to that calculus and domain.

---

## Proof

Let `F` be a FAR representation with calculus `C` and transition domain `D`.

Assume:

```text
For every transition t in D, if C permits t, then F contains a transition signature for t.
```

Let `t` be an arbitrary transition in `D` permitted by `C`.

By the assumption, `F` contains a transition signature for `t`.

Therefore every `C`-permitted transition in `D` is represented in `F`.

By definition, a FAR representation is complete relative to `C` and `D` when it represents every transition permitted by `C` in `D`.

Therefore `F` is complete relative to `C` and `D`.

---

## Corollary

Completeness in FAR is never unqualified. It is relative to a calculus and a transition domain.

---

## Limitation

The theorem does not cover transitions outside the specified domain or transitions that are permitted by an unstated calculus.
