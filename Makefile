health:
	python tools/repo_health_check.py --full
	python tools/check_research_gates.py
	python tools/check_deduction_first_program.py
	python tools/check_thm_target_001.py
	python tools/check_faithful_representation.py
	python tools/check_p8_theorem_role.py
	python tools/check_s_core_lemma_ledger.py
	python tools/check_s_core_w0.py
	python tools/check_s_core_w1.py
	python tools/check_s_core_w2.py
	python tools/check_s_core_w3.py
	python tools/check_s_core_w4.py
	python tools/check_representation_discovery_separation.py
	python tools/check_candidate_architectures.py
	python tools/check_reasoning_domain.py
	python tools/check_independent_reasoning_definition.py
	python tools/check_preservation_basis.py
	python tools/check_pb001_test_suite.py
	python tools/check_pb001_execution.py
	python tools/check_pbts001_replication_package.py
	python tools/check_pbts001_replication_run001_controls.py

health-fast:
	python tools/repo_health_check.py --fast
	python tools/check_research_gates.py
	python tools/check_deduction_first_program.py
	python tools/check_thm_target_001.py
	python tools/check_faithful_representation.py
	python tools/check_p8_theorem_role.py
	python tools/check_s_core_lemma_ledger.py
	python tools/check_s_core_w0.py
	python tools/check_s_core_w1.py
	python tools/check_s_core_w2.py
	python tools/check_s_core_w3.py
	python tools/check_s_core_w4.py
	python tools/check_representation_discovery_separation.py
	python tools/check_candidate_architectures.py
	python tools/check_reasoning_domain.py
	python tools/check_independent_reasoning_definition.py
	python tools/check_preservation_basis.py
	python tools/check_pb001_test_suite.py
	python tools/check_pb001_execution.py
	python tools/check_pbts001_replication_package.py
	python tools/check_pbts001_replication_run001_controls.py

docs-check:
	python tools/validate_docs.py

links-check:
	python tools/check_internal_links.py

math-check:
	python tools/check_math_rendering.py

release-check:
	python tools/check_release_consistency.py

research-check:
	python tools/check_research_gates.py
	python tools/check_deduction_first_program.py
	python tools/check_thm_target_001.py
	python tools/check_faithful_representation.py
	python tools/check_p8_theorem_role.py
	python tools/check_s_core_lemma_ledger.py
	python tools/check_s_core_w0.py
	python tools/check_s_core_w1.py
	python tools/check_s_core_w2.py
	python tools/check_s_core_w3.py
	python tools/check_s_core_w4.py
	python tools/check_representation_discovery_separation.py
	python tools/check_candidate_architectures.py
	python tools/check_reasoning_domain.py
	python tools/check_independent_reasoning_definition.py
	python tools/check_preservation_basis.py
	python tools/check_pb001_test_suite.py
	python tools/check_pb001_execution.py
	python tools/check_pbts001_replication_package.py
	python tools/check_pbts001_replication_run001_controls.py

status:
	python tools/project_status_report.py

gaps:
	python tools/detect_research_gaps.py

plan:
	python tools/self_advancement_plan.py


dashboard:
	python tools/self_advancement_plan.py

release-readiness:
	python tools/release_readiness_report.py

test:
	python tools/run_tests.py

test-fast:
	python tools/run_tests.py --fast

validate:
	python -m far_validation validate --profile pr-fast

validate-changed:
	python -m far_validation validate --profile pr-fast --changed origin/main --explain

validate-full:
	python -m far_validation validate --profile pr-full

validate-release:
	python -m far_validation validate --profile release --no-cache

validate-doctor:
	python -m far_validation doctor

validate-diagnose:
	python -m far_validation diagnose

validate-trace:
	python -m far_validation validate --profile pr-full --no-cache --trace-dependencies --require-trace

validate-oracle:
	python -m far_validation oracle

validate-weakening:
	python -m far_validation weakening --base origin/main

validate-mutations:
	python -m far_validation mutations --report artifacts/validation/runtime/mutation-campaign.json

validate-formal:
	python -m far_validation formal --max-checks 4
	lean mechanization/lean/ValidationEngine.lean

validate-assurance:
	python validation_bootstrap/verify.py
	python -m unittest discover -s tests -p "test_validation_assurance.py" -v
	python -m far_validation oracle
	python -m far_validation weakening --base origin/main
	python -m far_validation formal --max-checks 4
	python -m far_validation mutations --report artifacts/validation/runtime/mutation-campaign.json

validate-certificate:
	python -m far_validation certificate verify --require-signed --expected-commit "$$(git rev-parse HEAD)" --expected-tree "$$(git rev-parse HEAD^{tree})"

cre001-deterministic:
	python tools/cre001_compile_vocabularies.py --write --check

cre002-execute:
	python tools/cre002_execute.py --write --check
