# FAR Epistemic Assurance Promotion Acceptance v1.0

Status: Accepted  
Origin investigation: `FAR-SAT-v0.4`  
Promotion scope: composable assurance contracts only  
Baseline ref: `4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a`

## Accepted requirements

The repository-first saturation delta established four representational gaps and one cross-cutting control boundary that could not be losslessly reduced to existing canonical contracts:

1. source-dependence lineage;
2. bitemporal evidence/source state;
3. deliberate verifier abstention;
4. audit self-assurance profile;
5. hostile-source content isolation.

The discovery, falsification, and replication records are:

- `research/discovery/FAR-SAT-v0.4/README.md`
- `research/discovery/FAR-SAT-v0.4/falsification.md`
- `research/replications/epistemic-assurance/FAR-SAT-v0.4-replication.md`

## Authorized promotion

The accepted requirements are promoted through:

- `schemas/far-source-lineage-v1.schema.json`
- `schemas/far-temporal-state-v1.schema.json`
- `schemas/far-abstention-v1.schema.json`
- `schemas/far-audit-assurance-v1.schema.json`
- `methodology/hostile-source-boundary.md`
- `far_validation/epistemic_assurance.py`
- `tests/test_epistemic_assurance.py`

## Nonclaims

This acceptance does not establish:

- external empirical utility;
- completeness of the saturation harvest for all future knowledge;
- source truth from source lineage;
- truth from temporal state;
- truth from audit assurance;
- calibrated probability merely because an abstention record exists;
- safety against every adversarial input;
- a replacement for existing FAR/FARA/FARO theory.

## Compatibility

Existing v1 contracts remain unchanged. The promoted contracts are additive and composable. Where an existing record already supplies a distinction, that record remains authoritative; these contracts must not duplicate or overwrite it.

## Reopening conditions

Reopen this acceptance if:

- an existing canonical contract is shown to represent one of the promoted distinctions losslessly;
- semantic tests demonstrate contradictory authority;
- a promoted contract cannot survive practical use without changing accepted theory;
- a new execution exposes an unrepresented assurance distinction.
