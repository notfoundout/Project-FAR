# Project FAR v0.3 — Automation Roadmap

## Status

Roadmap milestone.

## Date

2026-07-06

---

# Purpose

Project FAR v0.3 targets the transition from manual theory governance to automated theory verification.

Version 0.2 established proof standards, theorem lifecycle rules, dependency tracking, registry requirements, falsification tests, and worked encodings. Version 0.3 begins enforcing those standards with machine-readable metadata and scripts.

---

# Automation Layer Added

The initial automation layer consists of:

- `theory/metadata/theorems.yaml`
- `tools/verify_theory.py`
- `tools/generate_theorem_index.py`
- `tools/check_dependencies.py`
- `tools/check_registry.py`
- `tools/check_notation.py`
- `tools/check_circularity.py`
- `.github/workflows/repo-health.yml`
- `requirements.txt`

---

# Current Verification Capabilities

The verifier checks that:

1. every theorem metadata entry has required fields;
2. every theorem metadata entry uses an allowed status;
3. every theorem has a proof file;
4. every theorem listed in the catalog has metadata;
5. every theorem listed in the catalog has a proof file;
6. theorem dependencies resolve to known identifiers or canonical resources;
7. no theorem directly depends on itself;
8. the theorem dependency graph contains no cycles;
9. derived concepts listed in theorem metadata are registered;
10. canonical notation contains required symbols;
11. theorem index generation works from metadata.

---

# Current Limits

The automation layer does not yet prove theorem correctness.

It verifies repository consistency, dependency discipline, registry coverage, notation availability, and circularity structure.

It cannot yet decide whether a proof step is logically valid. That requires either stricter proof syntax, a proof assistant, or a custom formal checker.

---

# v0.3 Completion Targets

To complete v0.3, the project should add:

1. machine-readable proposition metadata;
2. machine-readable lemma metadata;
3. generated theorem catalog replacement or sync check;
4. generated dependency graph replacement or sync check;
5. proof-file schema validation;
6. theorem status transition validation;
7. automatic stale-index detection;
8. exact registry coverage checks for proof text, not only metadata;
9. notation usage checks over proof text;
10. first proof-assistant prototype or formal grammar.

---

# v0.4 Direction

The next major step after v0.3 is formalization.

Candidate paths:

- Lean prototype;
- Coq prototype;
- TLA+/Alloy model checking for dependency structures;
- custom typed proof DSL;
- Python-based proof object checker.

---

# Milestone Assessment

Project FAR now has the beginning of enforceable theory governance.

The project has moved from manual documentation discipline toward automated structural verification.

This does not make the theory proven in a machine-checkable mathematical sense yet. It makes the repository harder to corrupt, easier to audit, and ready for deeper formalization.
