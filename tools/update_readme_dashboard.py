#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]; P=R/'README.md'; B='<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->'; E='<!-- END GENERATED PROJECT FAR DASHBOARD -->'
def j(p): return json.loads((R/p).read_text())
def generate_index(): return None
def block():
 s=j('theory/evaluation/reasoning-and-contrast-scope-v1.0.json'); d=j('theory/evaluation/w3-5-factorization-result-v1.0.json')['dimensions']; x=j('theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json')['registered_results']; q=j('theory/evaluation/w3-5-fara-specificity-result-v1.0.json')['result']; c=j('theory/evaluation/w3-5-candidate-test-result-v1.0.json'); a=c['axis_counts']['structural_commitment_necessity']; n=(len(s['positive_instances']),len(s['contrast_instances']),len(s['disputed_instances']))
 return f'''{B}

## Repository Status

- Current project phase: W3.5 candidate evidence-complete re-execution
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- W5 status: blocked by incomplete `W3.5-SDG-001`

## Track Status

| Track | Status | Current boundary |
|---|---|---|
| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |
| ADJ | Corpus, factorization, discrimination, and specificity complete; candidate execution incomplete | {n[0]} positive, {n[1]} contrast, {n[2]} disputed; 0/648 candidate trials preserved |
| USD | Target frozen | Structural indispensability unresolved for all 12 candidates |
| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |

## Registered ADJ Results

- Factorization interpretation: `{d['overall_interpretation']}`.
- Reasoning discrimination: {x['positive']['reasoning_like']}/8 positives reasoning-like; {x['contrast']['nonreasoning_like']}/8 contrasts nonreasoning-like; {x['disputed']['borderline']}/2 disputed borderline.
- FARA-specificity classification: `{q['classification']}`.
- Candidate result: `{c['aggregate_result']}`.
- Structural necessity: unresolved {a['unresolved']}; supported {a['supported_at_registered_scope']}; refuted {a['refuted_at_registered_scope']}; partial {a['partial']}.
- Candidate evidence: preliminary internal adjudication; atomic ablation/reconstruction evidence missing.

## Top Priority Tasks

### STRATEGIC-003: Execute candidate ablation and reconstruction

- Preserve all 648 candidate × case × representation trials with explicit ablation, reconstruction, equivalence, equivalent-reintroduction, and machinery-cost records.

### STRATEGIC-004: Complete W3.5 closure

- Complete cost, claim-impact, and preserved-failure artifacts only after candidate execution is evidence-complete.

## Current Roadmap

- REP: W0-W4 complete at bounded `S_core` scope.
- ADJ: execute evidence-complete candidate testing; do not promote preliminary observations.
- USD: universal structure remains unresolved.
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

{E}
'''
def main():
 t=P.read_text(); g=block().strip(); P.write_text((re.sub(re.escape(B)+r'.*?'+re.escape(E),g,t,flags=re.S)).rstrip()+'\n'); print('README.md dashboard updated')
if __name__=='__main__': main()
