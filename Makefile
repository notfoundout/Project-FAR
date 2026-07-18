health:
	python tools/repo_health_check.py --full
	python tools/check_research_gates.py
	python tools/check_candidate_architectures.py

health-fast:
	python tools/repo_health_check.py --fast
	python tools/check_research_gates.py
	python tools/check_candidate_architectures.py

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
	python tools/check_candidate_architectures.py

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

cre001-deterministic:
	python tools/cre001_compile_vocabularies.py --write --check

cre002-execute:
	python tools/cre002_execute.py --write --check
