#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]; P=R/'README.md'; B='<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->'; E='<!-- END GENERATED PROJECT FAR DASHBOARD -->'
def j(p): return json.loads((R/p).read_text())
def generate_index(): return None
def block():
 s=j('theory/evaluation/reasoning-and-contrast-scope-v1.0.json'); d=j('theory/evaluation/w3-5-factorization-result-v1.0.json')['dimensions']; x=j('theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json')['registered_results']; q=j('theory/evaluation/w3-5-fara-specificity-result-v1.0.json')['result']; n=(len(s['positive_instances']),len(s['contrast_instances']),len(s['disputed_instances']))
 return f'''{B}

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: W3.5 candidate testing, reconstruction, full cost accounting, and claim closure
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | W3.5 in progress; corpus, factorization, discrimination, and specificity complete | {n[0]} positive, {n[1]} contrast, {n[2]} disputed; candidate, cost, and claim closure pending |
| USD | Target frozen, unexecuted | No universal-structure candidate classified |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

No aggregate completion percentage is authorized across REP, ADJ, and USD.

## Registered ADJ Results

- Factorization expressiveness: `{d['expressiveness']}`.
- Factorization translation: `{d['translation']}`.
- Factorization constraint strength: `{d['constraint_strength']}`.
- Factorization reasoning specificity: `{d['reasoning_specificity']}`.
- Factorization cost relation: `{d['cost_relation']}`.
- Factorization interpretation: `{d['overall_interpretation']}`.
- Reasoning discrimination: {x['positive']['reasoning_like']}/8 positives reasoning-like; {x['contrast']['nonreasoning_like']}/8 contrasts nonreasoning-like; {x['disputed']['borderline']}/2 disputed borderline.
- FARA-specificity classification: `{q['classification']}`.
- Unique FARA discriminative capacity: `{q['unique_discriminative_capacity_of_fara']}`.
- Boundary: project-authored, non-blind semantic licensing over a finite synthetic corpus; no population inference, FARA necessity, or universal definition is claimed.

## Top Priority Tasks

### STRATEGIC-003: Execute candidate ablation and reconstruction

- Test every universal-structure hypothesis across the frozen corpus and alternative conceptual bases, counting equivalent reintroduction and preserving counterexamples.

### STRATEGIC-004: Complete W3.5 cost and claim-impact audit

- Produce complete machinery accounting, preserved failures, immutable links, and track-specific claim effects without erasing the qualified-negative specificity result.

### STRATEGIC-005: Assemble W5

- Blocked until all remaining W3.5 artifacts are complete.

## Universal-Structure Discovery

- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)
- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)
- Frozen concrete corpus: [RCS-CORPUS-001](docs/research/w3-5-concrete-corpus-freeze-v1.0.md)
- Factorization result: [W35-FACTOR-RESULT-001](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- Discrimination and specificity result: [W35-SCOPE-RESULT-001 / W35-SPEC-RESULT-001](docs/research/w3-5-reasoning-discrimination-and-specificity-v1.0.md)
- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)
- Current candidate result: unresolved

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Next Actions](docs/planning/next-actions.md)
- [GREL-FARA Factorization](docs/research/w3-5-grel-fara-factorization-v1.0.md)
- [Reasoning Discrimination and Specificity](docs/research/w3-5-reasoning-discrimination-and-specificity-v1.0.md)
- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)
- [Central Claim Registry](theory/evaluation/central-claim-registry.json)
- [Research Gates](theory/evaluation/research-gates.json)

## Current Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: corpus, factorization, registered discrimination, and qualified specificity complete; execute candidate testing, reconstruction, full cost, failure, and claim closure.
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
4. Do not promote bounded discrimination into universal-structure or necessity status.
5. Run full health before merge.

{E}
'''
def main():
 t=P.read_text(); g=block().strip(); P.write_text((re.sub(re.escape(B)+r'.*?'+re.escape(E),g,t,flags=re.S)).rstrip()+'\n'); print('README.md dashboard updated')
if __name__=='__main__': main()
