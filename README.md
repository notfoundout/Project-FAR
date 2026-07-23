# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

## Central result

The registered Universal Proof Program `POST-TUE-UPP-001` is complete. Its terminal adjudication is:

`strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary`

The proved result is relative and operational. For systems and representations satisfying the independently frozen target-class, admissibility, faithfulness, machinery-closure, and commitment-equivalence premises, the registered construction recovers an RCCD-equivalent package preserving structural, semantic, operational, dependency, informational, historical, registered-query, and failure/Unknown commitments.

The result is deliberately weaker than unrestricted universality because:

- maximality is established only under frozen extension rules and a finite registered challenge ledger;
- the end-to-end semantic theorem is compositionally and executably checked, but not represented as one kernel-checked proof object;
- no metaphysical, open-world, uniqueness, consciousness, or final-ontology claim is licensed.

Public evaluation is authorized only when the exact theorem, premises, mechanization status, open-world boundary, Unknown discipline, and nonclaims are disclosed together.

- [Terminal theorem disclosure](docs/research/upp-w15-terminal-theorem-v1.0.md)
- [Terminal theorem audit](docs/audits/upp-w15-terminal-theorem-audit.md)
- [Post-terminal public-evaluation program](docs/governance/post-terminal-public-evaluation-program-v1.0.md)
- [Central research program](docs/governance/central-research-program.md)

## Research tracks

Project FAR retains three distinct evidence tracks:

- **REP:** bounded representation capacity and fidelity;
- **ADJ:** baseline factorization, specificity, ablation, reconstruction, and cost;
- **USD/UPP:** architecture-neutral universal-structure discovery and the completed relative RCCD theorem program.

Earlier REP and ADJ artifacts remain bounded evidence. They are not retroactively promoted into the terminal theorem and remain governed by their original assumptions and nonclaims.

## Current phase

The deductive queue is closed. The repository is now in **post-terminal evaluation and replication**.

Current priorities:

1. expose the exact weakened theorem to independent criticism and countermodel search;
2. obtain independent proof review and, where possible, kernel-checked reconstruction of the complete semantic composition;
3. execute independent empirical replication tracks without treating them as deductive proof;
4. register every counterexample, failed reconstruction, ambiguity, and scope challenge as immutable evidence;
5. revise or retract claims when registered evidence defeats a premise or construction.

The next phase does not add a fictitious `UPP-W16`. Any new deductive claim requires a new registered program with independently frozen scope, assumptions, outcomes, and stopping rules.

## Repository commands

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
python tools/check_post_terminal_public_evaluation.py
```

## Mechanization MVP

Phase 3 mechanization provides an executable MVP for the `far-ir/1.0` interchange format. It includes a canonical Python IR, JSON/YAML parsing, deterministic normalization and serialization, graph construction and dependency validation, structured diagnostics, a CLI, and a versioned conformance suite.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
far version
far validate examples/mechanization/minimal-investigation.json
far normalize examples/mechanization/minimal-investigation.json
far graph examples/mechanization/minimal-investigation.json
python -m mechanization.far_mechanization.conformance
```

The MVP does not by itself verify the terminal theorem or establish application correspondence.