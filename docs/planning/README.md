# Project FAR Self-Advancement Planner

The root [README Command Center](../../README.md) is the canonical entry point for Project FAR planning; this page is a secondary planning index.

The self-advancement planner is an advisory reporting system. It inspects existing registries and reports, preserves a generated historical bounded-program snapshot, detects research gaps, and drafts program-scoped next tasks. It is not a current-state authority.

Current project state is governed by [`docs/project-status.md`](../project-status.md), the root README, the canonical map, and applicable governance artifacts. The planner may recommend work, but it does not authorize theory, evidence, experiment, or claim-status changes.

## Current Foundation Checkpoint

The strict validation pass from AX-001 through T-001 is consolidated in [Foundation Validation Consolidation](../reports/foundation-validation-consolidation.md).

That consolidation is a navigation and status artifact only. It does not modify theory content or authorize automatic promotion.

## What It Does

- Reads machine-readable evaluation and falsification registries.
- Generates `docs/reports/project-status-generated.md` as an explicitly historical W3.5-era bounded snapshot, not current project status.
- Detects possible gaps in `docs/reports/research-gap-report.md`.
- Generates advisory next actions in `docs/planning/next-actions.md` from the registered `POST-TERM-EVAL-001` workstreams.

## What It Does Not Do

- It does not override `docs/project-status.md` or resolve conflicts between canonical authority surfaces.
- It does not change primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, or evaluation conclusions.
- It does not prove unrestricted universality, independence, minimality, or application correspondence.
- It does not reopen the completed `POST-TUE-UPP-001` deductive queue.
- It does not authorize implementation, empirical execution, theory changes, or claim promotion.

## How to Run

```bash
python tools/self_advancement_plan.py
```

Individual reports can also be regenerated with:

```bash
python tools/project_status_report.py
python tools/detect_research_gaps.py
python tools/generate_next_tasks.py
```

If Make targets are available, run:

```bash
make plan
```

## How to Interpret Reports

Treat generated reports as planning aids. `docs/reports/project-status-generated.md` is historical by construction. Gap severity indicates review urgency, not truth. Recommended actions are bounded by the current registered program and still require the applicable Charter and governance gates before execution.

If generated output conflicts with a current canonical authority surface, report the conflict; do not let generated output break the tie.

## Why Governance Review Is Required

Project FAR's Research Execution Charter requires objective evidence, reproducibility, falsification, provenance, and the governed discovery lifecycle before acceptance or promotion. Automated planning can route attention, but it cannot determine acceptance, promotion, independence, or theorem validity.
