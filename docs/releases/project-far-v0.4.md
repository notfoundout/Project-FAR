# Project FAR v0.4 — Formalization and Prototype Tooling

## Status

Active roadmap milestone.

## Purpose

Project FAR v0.4 begins the transition from structural repository verification to executable formalization.

v0.3 verified that theory files are organized consistently. v0.4 begins defining the formal language, semantics, proof objects, parser, proof checker, reasoning engine, and proof-assistant scaffold.

---

# Added in v0.4 Start

## Formal Language

`theory/formal-language/far-language.md`

Defines:

- primitive sorts;
- FAR tuple syntax;
- representation syntax;
- structure syntax;
- interpretation syntax;
- calculus syntax;
- trace syntax;
- well-formed FAR objects.

## Formal Semantics

`theory/formal-semantics/far-semantics.md`

Defines:

- FAR model satisfaction `A ⊨ φ`;
- syntax/semantics distinction;
- represented/interpreted/admissible conditions;
- semantic failure.

## Proof Objects

`theory/proof-objects/proof-object-schema.yaml`

Defines a first machine-readable proof object schema.

## Parser

`tools/parse_far.py`

Parses FAR YAML files into internal data structures.

## Proof Checker

`tools/check_proof_object.py`

Checks structural validity of machine-readable proof objects.

## Reasoning Engine Prototype

`tools/reasoning_engine.py`

Loads a FAR object, checks well-formedness, builds dependency edges, detects cycles, and prints derivation trees.

## Mechanization Scaffold

`mechanization/lean/FARCore.lean`

Provides an initial Lean scaffold for FAR primitives and the representation theorem.

---

# Current Boundary

The parser and proof checker are prototypes.

They check structure, references, step order, and dependency availability. They do not yet prove arbitrary natural-language proof steps.

The Lean file is a scaffold using axiom placeholders. It is not yet a fully reduced proof of the theorem catalog.

---

# v0.4 Completion Targets

1. Add CI checks for FAR YAML examples.
2. Add CI checks for proof-object YAML files.
3. Add proposition and lemma metadata.
4. Add generated indexes for propositions and lemmas.
5. Add proof-step rule semantics.
6. Add more machine-readable FAR examples.
7. Replace axiom placeholders in Lean with explicit structures where possible.
8. Mechanize T-003 completely.
9. Add test fixtures for valid and invalid FAR objects.
10. Define a formal grammar for FAR YAML.

---

# Real v0.3 Tag Note

The repository contains `docs/releases/v0.3-release-marker.md`, but a real Git tag or GitHub Release still needs to be created through the GitHub UI or Git CLI because the current connector does not expose a release/tag creation action.
