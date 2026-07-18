# Architecture-Neutral Reset Audit

## Scope

This audit records the repository dependency decisions used to complete the architecture-neutral reset after PRs #209 and #210.

## Authoritative baseline preserved

The following remain authoritative and were not replaced:

- `docs/governance/central-research-program.md`
- `docs/governance/anti-self-validation-standard.md`
- `docs/governance/research-priority-reset.md`
- `docs/governance/evidence-replication-and-freeze-standard-v1.0.md`
- the external observation, negative-control, comparative-cost, anti-reintroduction, boundary-discovery, and confirmatory-package standards;
- `theory/evaluation/central-claim-registry.json`;
- `theory/evaluation/research-gates.json`;
- CRE-004 blinding and coordinator controls.

## Dependency findings

1. The Central Research Program already defined the architecture-neutral central question and permitted unfavorable conclusions.
2. The Research Priority Reset already established falsifiable gates and stop conditions.
3. The missing layer was a canonical operational distinction among Project FAR, FARA, FARO, candidate architectures, evaluation machinery, and the future discovery system.
4. The repository already uses `docs/governance/` for controlling standards, `docs/architecture/` for architectural decisions, `docs/planning/` for ordered work, and `theory/evaluation/` for machine-readable research state. The new artifacts follow those demonstrated dependencies.
5. FARA remains mathematically defined by existing Foundation and theory artifacts. This reset adds governance metadata only.
6. FARO retains its existing operational role. It is not promoted to an independent theory or evidence source.
7. The future independent reasoning-domain specification is deliberately upstream of FARA to prevent circular validation.

## Terminology collisions

Historical uses of “FAR” may refer to the project, candidate architecture, vocabulary, or machinery. Global rewriting would risk changing historical claims. The reset therefore applies explicit terminology prospectively while preserving frozen results.

## Files added

### Governance

- `docs/governance/research-architecture.md`
- `docs/governance/candidate-architecture-standard-v1.0.md`

### Registry

- `theory/evaluation/candidate-architecture-registry.json`

### Architecture and planning

- `docs/architecture/architecture-neutral-research-engine-blueprint.md`
- `docs/planning/architecture-neutral-research-roadmap.md`

### Enforcement

- `tools/check_candidate_architectures.py`
- Makefile integration with `health`, `health-fast`, and `research-check`

## Scientific nonclaims

This reset does not:

- define reasoning independently;
- prove that a universal structure exists;
- prove FARA universal or minimal;
- establish primitive necessity;
- close the candidate search space;
- resolve the six-dimensional preservation basis;
- implement exhaustive search;
- establish independent replication;
- alter historical experiment results.

## Current scientific status

- existence: unresolved;
- bounded sufficiency: only as currently registered;
- universality: not established;
- necessity: not established;
- minimality: not established;
- comparative economy: not established;
- general independent replication: not established.

## Next scientific PR

Construct and freeze an architecture-neutral definition or specification of the reasoning-system class to be tested, without deriving its required structure from FARA.
