# Project FAR Self-Advancement Planner

The root [README Command Center](../../README.md) is the canonical entry point for Project FAR planning; this page is a secondary planning index.
The self-advancement planner is an advisory reporting system. It inspects existing registries and reports, summarizes the current repository status, detects research gaps, and drafts recommended next tasks for human approval.

The planner may recommend theory work, but it does not authorize theory changes.

## Current Foundation Checkpoint

The strict validation pass from AX-001 through T-001 is consolidated in [Foundation Validation Consolidation](../reports/foundation-validation-consolidation.md).

That consolidation is a navigation and status artifact only. It does not modify theory content or authorize automatic promotion.

## What It Does

- Reads machine-readable evaluation and falsification registries.
- Summarizes current status in `docs/reports/project-status-generated.md`.
- Detects possible gaps in `docs/reports/research-gap-report.md`.
- Generates advisory next actions and task briefs in `docs/planning/next-actions.md`.

## What It Does Not Do

- It does not change primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, or evaluation conclusions.
- It does not prove FAR universal.
- It does not authorize implementation or theory changes.

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

Treat generated reports as planning aids. Gap severity indicates review urgency, not truth. Recommended actions identify possible next work, but humans must approve any change that would affect theory or conclusions.

## Why Human Approval Is Required

Project FAR's research charter requires objective evidence, reproducibility, falsification, and human review before accepted theory changes. Automated planning can highlight evidence, but it cannot determine acceptance or promotion.
