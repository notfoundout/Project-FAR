# Internal Consistency Report

Status: Provisional v0.3.0 report.

## Purpose

This report summarizes repository-supported internal consistency checks relevant to the v0.3.0 primitive-sufficiency baseline. It distinguishes machine-checked results from manual review and unresolved items.

## Check Table

| Check | Source Tool or Document | Status | Notes |
|---|---|---|---|
| Theorem dependency checks | `python tools/check_dependencies.py` | machine-checked | Validates theorem dependency references in the current repository. |
| Proof-object validation | `python tools/verify_theory.py`; `tools/check_proof_object.py` | machine-checked through theory verifier | The verifier exercises proof-object validation for current proof artifacts. |
| Metadata validation | `python tools/verify_theory.py`; current metadata files | machine-checked through theory verifier | No metadata schema changes were made for v0.3.0 completion. |
| Registry validation | `python tools/check_registry.py` | machine-checked | Validates theorem/registry consistency. |
| Circularity checks | `python tools/check_circularity.py` | machine-checked | Checks dependency cycles according to current tool behavior. |
| Notation checks | `python tools/check_notation.py` | machine-checked | Checks notation according to current notation validation tool. |
| Theorem index generation | `python tools/generate_theorem_index.py` | machine-generated validation artifact | Regenerates theorem index from current theorem metadata. |
| Reasoning-system fixture evaluation | `python tools/evaluate_reasoning_systems.py` | machine-checked | Evaluates all current reasoning-system fixtures. |
| Primitive-sufficiency registry checks | `python tools/evaluate_primitive_sufficiency.py` | machine-checked | Regenerates primitive-sufficiency report statistics from current registries. |
| Adversarial registry checks | `python tools/run_adversarial_suite.py` | machine-checked | Summarizes adversarial suite status and pressure counts. |
| Evaluation consistency checks | `python tools/check_evaluation_consistency.py` | machine-checked | Validates only evaluation/reporting registries: required fields, known classifications/statuses, duplicate IDs, fixture existence, and primitive names. |
| Cross-domain classification consistency | `theory/evaluation/cross-domain-consistency.md`; `docs/reports/cross-domain-audit.md` | manually reviewed | No direct contradiction found; borderline cases remain documented. |
| Primitive independence | `theory/evaluation/primitive-independence.md` | manually reviewed | Provisional repository-grounded argument only; not a formal independence proof. |
| Minimality | `theory/evaluation/minimality.md` | manually reviewed | Provisional non-redundancy only; not a formal proof of minimality. |
| FAR example parsing | `python tools/parse_far.py examples/far/*.far.yaml examples/far/reasoning-systems/*.far.yaml` | machine-checked | Confirms current example fixtures parse under current parser. |
| Reasoning-engine smoke tests | `python tools/reasoning_engine.py examples/far/modus-ponens-ascii-conditional.far.yaml`; `python tools/reasoning_engine.py examples/far/syllogism.far.yaml` | machine-checked | Exercises current reasoning-engine behavior against smoke fixtures. |

## Current Conclusion

The available validation tools support the claim that v0.3.0 documentation and evaluation updates did not introduce detected theorem dependency, registry, circularity, notation, parsing, adversarial-registry, or primitive-sufficiency-registry inconsistencies. Cross-domain consistency, primitive independence, and minimality remain documented manual analyses. No report here claims machine proof where only manual review exists.
