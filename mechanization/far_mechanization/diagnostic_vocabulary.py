"""Published diagnostic vocabularies for ``far-ir/2.0`` and ``far-ir/2.1``.

The diagnostic codes a verifier emits are part of the published interchange surface, not
internal implementation detail: ``EFR-R2`` requires two clean-room implementations to agree
with the frozen expected result on error category for every item, using only the published
specifications. That criterion is unsatisfiable while the vocabulary is unpublished.

This module is a **read-only declaration**, deliberately separate from the verifiers:

* ``mechanization/far_mechanization/contract_v2.py`` is pinned by git blob identity as the
  preregistered ``PCA-W6`` protocol base and must not change after that freeze;
* ``mechanization/far_mechanization/contract_v21.py`` is pinned by SHA-256 in the completed
  ``PCA-W5`` campaign manifest.

Publishing the vocabulary is therefore done here rather than by editing either verifier, so no
frozen protocol base or completed-campaign manifest is disturbed. Nothing in this module is
imported by the verifiers and it cannot change their behavior.

``tests/test_far_contract_diagnostic_codes.py`` holds these sets equal to the codes the
verifier sources actually emit and to the tables published in the specifications.

Publishing the vocabulary is a specification-completeness obligation. It is not a claim that
either code set is minimal, complete for future versions, or externally validated.
"""
from __future__ import annotations

#: Diagnostic codes emitted by the ``far-ir/2.0`` verifier.
#: Published in ``docs/specification/far-ir-2.0-contract.md`` section 9.
FAR_IR_2_0_DIAGNOSTIC_CODES: frozenset[str] = frozenset({
    "CASE_TABLE_COVERAGE_MISMATCH",
    "CHECKED_EVIDENCE_OUTCOME_MISMATCH",
    "CHECK_REQUIRES_EXPLICIT_TABLES",
    "CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN",
    "COLLISION_BEHAVIOR_AGREES",
    "COLLISION_CASE_UNKNOWN",
    "COLLISION_REPRESENTATION_DIFFERS",
    "COLLISION_REQUIRES_DISTINCT_CASES",
    "DECODER_UNDEFINED",
    "DUPLICATE_CASE_VALUE",
    "DUPLICATE_DOMAIN_CASE",
    "DUPLICATE_OBSERVATION_CONTEXT",
    "DUPLICATE_TRANSFORMATION",
    "FACTORIZATION_FAILURE",
    "FREEZE_HASH_MISMATCH",
    "NONFUNCTIONAL_DECODER",
    "QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT",
    "QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL",
    "QUOTIENT_NOT_PARTITION",
    "QUOTIENT_OVERLAP",
    "SCHEMA_CONSTRAINT_VIOLATION",
    "UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME",
    "UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME",
    "UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE",
    "UNREADABLE_CONTRACT",
    "W5_SEMANTICS_NOT_ESTABLISHED",
})

#: Diagnostic codes emitted by the ``far-ir/2.1`` verifier.
#: Published in ``docs/specification/far-ir-2.1-approximation-cost.md``.
#:
#: ``DUPLICATE_METRIC_VALUE`` and ``DUPLICATE_LOSS_ACTION`` are composed at runtime by
#: ``contract_v21._unique_values`` as ``DUPLICATE_{label}`` and appear as no source literal.
FAR_IR_2_1_DIAGNOSTIC_CODES: frozenset[str] = frozenset({
    "CASE_TABLE_COVERAGE_MISMATCH",
    "CHECKED_EVIDENCE_OUTCOME_MISMATCH",
    "CHECK_REQUIRES_EXPLICIT_BEHAVIOR",
    "CHECK_REQUIRES_EXPLICIT_REPRESENTATION",
    "CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN",
    "CHECK_REQUIRES_FROZEN_CONTRACT",
    "COST_COVERAGE_MISMATCH",
    "DECODER_COVERAGE_MISMATCH",
    "DECODER_NOT_PROBABILITY",
    "DECODER_UNKNOWN_ACTION",
    "DUPLICATE_CANDIDATE",
    "DUPLICATE_CANDIDATE_COST",
    "DUPLICATE_CASE_VALUE",
    "DUPLICATE_COST_DIMENSION",
    "DUPLICATE_DECODER_ACTION",
    "DUPLICATE_DECODER_ENTRY",
    "DUPLICATE_DOMAIN_CASE",
    "DUPLICATE_LOSS_ACTION",
    "DUPLICATE_LOSS_ENTRY",
    "DUPLICATE_METRIC_ENTRY",
    "DUPLICATE_METRIC_VALUE",
    "DUPLICATE_REFERENCE_CASE",
    "EXACT_RECOVERY_SET_MISMATCH",
    "FEASIBLE_SET_MISMATCH",
    "FREEZE_HASH_MISMATCH",
    "LEAST_SET_MISMATCH",
    "LOSS_METRIC_MISMATCH",
    "LOSS_NOT_TOTAL",
    "METRIC_IDENTITY_FAILURE",
    "METRIC_LOSS_DOMAIN_MISMATCH",
    "METRIC_NOT_TOTAL",
    "METRIC_SEPARATION_FAILURE",
    "METRIC_SYMMETRY_FAILURE",
    "METRIC_TRIANGLE_FAILURE",
    "PARETO_SET_MISMATCH",
    "REFERENCE_COVERAGE_MISMATCH",
    "REFERENCE_NOT_PROBABILITY",
    "SCHEMA_CONSTRAINT_VIOLATION",
    "UNREADABLE_CONTRACT",
    "W5_MODE_EVIDENCE_REQUIRED",
    "ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE",
})
