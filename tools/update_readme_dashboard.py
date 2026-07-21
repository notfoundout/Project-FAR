#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]; P=R/'README.md'; B='<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->'; E='<!-- END GENERATED PROJECT FAR DASHBOARD -->'
def j(p): return json.loads((R/p).read_text())
def generate_index(): return None
def block():
 s=j('theory/evaluation/reasoning-and-contrast-scope-v1.0.json'); d=j('theory/evaluation/w3-5-factorization-result-v1.0.json')['dimensions']; n=(len(s['positive_instances']),len(s['contrast_instances']),len(s['disputed_instances']))
 return f'''{B}

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: W3.5 specificity, discrimination, candidate testing, reconstruction, and cost closure
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | W3.5 in progress; corpus and factorization complete | {n[0]} positive, {n[1]} contrast, {n[2]} disputed; specificity and execution pending |
| USD | Target frozen, unexecuted | No universal-structure candidate classified |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

No aggregate completion percentage is authorized across REP, ADJ, and USD.

## Factorization Result

- Expressiveness: `{d['expressiveness']}`.
- Translation: `{d['translation']}`.
- Constraint strength: `{d['constraint_strength']}`.
- Reasoning specificity: `{d['reasoning_specificity']}`.
- Cost relation: `{d['cost_relation']}`.
- Overall interpretation: `{d['overall_interpretation']}`.
- Boundary: operational factorization only; the translation reuses the declared FARA-oriented adapter and accepted constructor, so no primitive reduction is claimed.

## Top Priority Tasks

### STRATEGIC-002: Execute reasoning/contrast discrimination and FARA specificity

- Test whether FARA constraints have a distinct reasoning-relevant role over the frozen corpus.

### STRATEGIC-003: Execute candidate ablation and reconstruction

- Test every candidate across the frozen corpus and alternative conceptual bases, counting equivalent reintroduction.

### STRATEGIC-004: Complete W3.5 cost and claim-impact audit

- Produce complete machinery accounting, preserved failures, and track-specific claim effects.

### STRATEGIC-005: Assemble W5

- Blocked until W3.5 resolves with complete immutable evidence.

## Universal-Structure Discovery

- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)
- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)
- Frozen concrete corpus: [RCS-CORPUS-001](docs/research/w3-5-concrete-corpus-freeze-v1.0.md)
- Factorization result: [W35-FACTOR-RESULT-001](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)
- Current candidate result: unresolved

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Next Actions](docs/planning/next-actions.md)
- [GREL–FARA Factorization](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)
- [Central Claim Registry](theory/evaluation/central-claim-registry.json)
- [Research Gates](theory/evaluation/research-gates.json)

## Current Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: corpus and factorization complete; execute specificity, discrimination, candidate testing, reconstruction, full cost, and claim impact.
- USD: keep every candidate unresolved until candidate-neutral execution.
- W5: blocked until W3.5 resolves with immutable evidence.

## Command Center

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
```

## Typical Workflow

1. Run `make research-check` and `make health-fast`.
2. Work only on an authorized REP, ADJ, or USD obligation.
3. Preserve countermodels, equivalences, reductions, failures, assumptions, and nonclaims.
4. Do not promote representation progress into universal-structure status.
5. Run full health before merge.

{E}
'''
def main():
 t=P.read_text(); g=block().strip(); P.write_text((re.sub(re.escape(B)+r'.*?'+re.escape(E),g,t,flags=re.S)).rstrip()+'\n'); print('README.md dashboard updated')
if __name__=='__main__': main()
