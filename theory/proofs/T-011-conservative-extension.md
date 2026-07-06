# T-011 — Conservative Extension Theorem

## Status

Established for definitionally conservative FAR extensions.

---

## Statement

If an extension `E` of Project FAR introduces no new primitive, alters no canonical definition, and changes no established axiom or theorem dependency, then `E` is conservative over the established core theory.

---

## Proof

Let `Core` be the established Project FAR theory and let `E` be an extension.

Assume:

1. `E` introduces no new primitive;
2. every new term in `E` is defined from existing primitives or established derived concepts;
3. `E` does not alter canonical definitions;
4. `E` does not alter established axioms;
5. `E` does not alter the dependency structure of established theorems.

Let `φ` be any theorem established in `Core`.

The proof of `φ` depends only on canonical definitions, axioms, propositions, and prior theorems in `Core`. By assumptions 3 through 5, those dependencies are unchanged by `E`.

Therefore the proof of `φ` remains valid after adding `E`.

Since `φ` was arbitrary, every established core theorem remains valid under `E`.

Therefore `E` is conservative over `Core`.

---

## Corollary

Future FAR modules should be accepted only if they are either conservative extensions or explicitly marked as revisionary.

---

## Limitation

This theorem does not prove that every useful extension is conservative. Some extensions may legitimately revise the core, but then they must be treated as theory revisions rather than ordinary modules.
