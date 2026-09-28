"""Which far-ir/2.0 verifier each tracked file may use.

Current verification is ``contract_v2_strict_v11`` (rule v1.1). The frozen baseline ``contract_v2``
stays byte-identical for historical provenance, and direct use of it is limited to the consumers
declared here. Rule v1.0, ``contract_v2_strict``, also stays byte-identical because the ``EFR-001``
comparator amendment v2.0 binds it. ``tests/test_contract_v2_verifier_authority.py`` scans every tracked file and
fails if a file outside this registry imports, dynamically loads, or invokes the baseline, or if
a registered consumer no longer references it.

See ``docs/specification/far-ir-2.0-current-verification.md``.
"""
from __future__ import annotations

CURRENT_FAR_IR_2_0_VERIFIER = "mechanization.far_mechanization.contract_v2_strict_v11"
FROZEN_FAR_IR_2_0_BASELINE = "mechanization.far_mechanization.contract_v2"

REASONS = frozenset({
    "baseline_self",
    "strict_wrapper",
    "errata_successor",
    "historical_pca_w6_protocol",
    "historical_efr_001_v1_0",
    "baseline_regression_test",
    "vocabulary_publication",
    "authority_enforcement",
})

#: Tracked files permitted to reference the frozen baseline directly, with the reason.
HISTORICAL_BASELINE_CONSUMERS: dict[str, str] = {
    "mechanization/far_mechanization/contract_v2.py": "baseline_self",
    "mechanization/far_mechanization/contract_v2_strict.py": "strict_wrapper",
    "mechanization/far_mechanization/contract_v2_errata1.py": "errata_successor",
    "mechanization/far_mechanization/verifier_authority.py": "authority_enforcement",
    "tests/test_contract_v2_verifier_authority.py": "authority_enforcement",
    "tools/check_pca_w6_empirical_audit_utility.py": "historical_pca_w6_protocol",
    "docs/research/pca-w6-empirical-audit-utility/00-preregistration.md": "historical_pca_w6_protocol",
    "docs/research/external-falsification-and-replication/02-u1-projection.md": "historical_efr_001_v1_0",
    "docs/governance/external-falsification-and-replication-program-v1.0.md": "historical_efr_001_v1_0",
    "theory/evaluation/external-falsification-and-replication-program-v1.0.json": "historical_efr_001_v1_0",
    "tests/test_efr_u1_projection.py": "historical_efr_001_v1_0",
    "tests/test_far_contract_v2.py": "baseline_regression_test",
    "tests/test_far_contract_v2_strict.py": "baseline_regression_test",
    "tests/test_far_contract_v2_errata1.py": "baseline_regression_test",
    "tests/test_local_jsonschema_keyword_coverage.py": "baseline_regression_test",
    "tests/test_efr_comparator_amendment.py": "baseline_regression_test",
    "tests/test_far_contract_diagnostic_codes.py": "vocabulary_publication",
}
