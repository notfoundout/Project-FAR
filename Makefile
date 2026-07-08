health:
	python tools/repo_health_check.py --full

health-fast:
	python tools/repo_health_check.py --fast

docs-check:
	python tools/validate_docs.py

links-check:
	python tools/check_internal_links.py

math-check:
	python tools/check_math_rendering.py

release-check:
	python tools/check_release_consistency.py

status:
	python tools/project_status_report.py

gaps:
	python tools/detect_research_gaps.py

plan:
	python tools/self_advancement_plan.py


dashboard:
	python tools/self_advancement_plan.py
