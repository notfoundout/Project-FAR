# T-011 — Conservative Extension Theorem

## Status

Established in revised definitionally conservative form.

---

## Statement

If an extension `E` of Project FAR introduces no new primitive, adds only terms or machinery definable from existing primitives or established derived concepts, alters no canonical definition, changes no established axiom or theorem statement, and changes no established theorem dependency, then every established core theorem retains its original proof under `E`. In this proof-preservation sense, `E` is conservative over the established core theory.

---

## Proof

Let `Core` be the established Project FAR theory and let `E` be an extension.

Assume:

1. `E` introduces no new primitive;
2. every new term or item of machinery in `E` is defined from existing primitives or established derived concepts;
3. `E` does not alter canonical definitions;
4. `E` does not alter established axioms;
5. `E` does not alter established theorem statements;
6. `E` does not alter the dependency structure of established theorems.

Let `φ` be any theorem established in `Core`.

The proof of `φ` depends only on canonical definitions, axioms, propositions, prior theorem statements, and theorem dependencies in `Core`. By assumptions 3 through 6, those proof inputs are unchanged by `E`.

By assumptions 1 and 2, and by the primitive sufficiency result for registered derived concepts, the additions made by `E` remain definitionally grounded in the existing Project FAR primitive architecture. They therefore add no new primitive basis from which an established core proof would need to be reinterpreted.

Therefore the original proof of `φ` remains valid after adding `E`.

Since `φ` was arbitrary, every established core theorem retains its original proof under `E`.

Therefore `E` is conservative over `Core` in the proof-preservation sense defined above.

---

## Corollary

Future FAR modules should be accepted only if they are either conservative extensions in this proof-preservation sense or explicitly marked as revisionary.

---

## Limitation

This theorem does not prove model-theoretic conservativity for arbitrary external semantics. It proves preservation of established Project FAR core proofs under definitionally grounded extensions that do not alter canonical definitions, established axioms, established theorem statements, or established theorem dependencies.

This theorem also does not prove that every useful extension is conservative. Some extensions may legitimately revise the core, but then they must be treated as theory revisions rather than ordinary modules.
