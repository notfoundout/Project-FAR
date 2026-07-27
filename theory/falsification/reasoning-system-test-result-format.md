# Reasoning-System Test Result Format

Status: Provisional

This document defines the machine-readable result format produced by `tools/evaluate_reasoning_systems.py`.

The evaluator classifies each fixture in `examples/far/reasoning-systems/` into exactly one of five statuses.

## Classifications

### `fits FAR`

The fixture is well formed, contains a complete mapping to the five FAR primitives, and declares that the tested reasoning system fits the current primitive architecture.

### `extends FAR`

The fixture is well formed and maps to the five FAR primitives, but the test indicates that additional derived concepts, domain-specific calculi, or conservative extensions are needed.

### `outside FAR scope`

The fixture is well formed enough to document a boundary case, but the tested process lacks the explicit representations, interpretation, or transition standards required by FAR's stated scope. This is a scope classification, not falsification evidence.

### `candidate counterexample`

The fixture is well formed and maps enough structure to be evaluated, but its declared verdict is that the system may falsify the current primitive architecture. A candidate counterexample is not automatically a successful falsification; it requires separate analysis showing that no conservative extension or derived-concept reduction is sufficient.

### `fails fixture`

The fixture cannot currently count as evidence. This occurs when it fails to parse, is not well formed, lacks a reasoning-system mapping, lacks a complete primitive mapping, or uses an unsupported verdict.

## JSON Shape

The evaluator emits this shape with `--json`:

```json
{
  "valid_classifications": [
    "candidate counterexample",
    "extends FAR",
    "fails fixture",
    "fits FAR",
    "outside FAR scope"
  ],
  "results": [
    {
      "fixture": "examples/far/reasoning-systems/classical-logic.far.yaml",
      "system": "Classical logic",
      "classification": "fits FAR",
      "primitive_mapping_complete": true,
      "representations": 3,
      "relations": 2,
      "transitions": 1,
      "cycles": 0,
      "notes": []
    }
  ]
}
```

## Evidence Rule

Only `fits FAR`, `extends FAR`, and `candidate counterexample` are evidence-bearing classifications about the primitive architecture.

`outside FAR scope` records a boundary without counting for or against primitive sufficiency. `fails fixture` means the test case itself must be corrected before any theoretical conclusion is drawn from it.
