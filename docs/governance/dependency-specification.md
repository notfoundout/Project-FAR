# Canonical Dependency Specification

Status: **Accepted and machine checked**

```text
foundations (0) → theory/shared (1) → FARA (2) → FAR (3) → FARO (4)
                                           ↘ downstream evidence/applications (5)
```

An artifact may cite a later layer for navigation, comparison, history, or a clearly labelled downstream consequence. It may not use that later layer as a definitional or proof prerequisite. Research proposals flow back only through the charter's acceptance/promotion lifecycle. Archive material is never canonical input.

The machine-readable rules are in [`semantic-consistency.json`](semantic-consistency.json); [`check_semantic_consistency.py`](../../tools/check_semantic_consistency.py) rejects reversed registered dependencies and duplicate term ownership.
