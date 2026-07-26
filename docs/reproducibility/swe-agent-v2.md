# Reproducing the SWE-agent v2 Evidence Check

Status: **Accepted reproducibility guide**

This guide verifies committed evidence; it does not rerun the model or claim to reproduce external provider behavior.

```bash
CASE=commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2
python "$CASE/evidence_pipeline_v2.py" verify-freeze
python "$CASE/verify_reveal_hardened.py" --output-dir "$CASE/post-freeze-reveal"
python tools/check_post_swe_agent_v2_stabilization.py
python -m unittest -v tests.test_post_swe_agent_v2_stabilization
```

The first command rehashes primary-freeze members and its sidecar. The second derives expected counts, decision, JSON report, Markdown report and bundle membership from the committed reveal and compares them exactly. The repository checker additionally validates current status wording, dependency direction, workflow timeout/failure/skip guards, canonical paths and local Markdown links.

Full source-tree verification additionally needs the exact external GitHub Actions artifact identified by `primary-freeze/source-artifact-lock.json`; pass its extracted directory to `evidence_pipeline_v2.py verify-source --artifact-root DIR`. A missing or expired artifact is an external reproducibility limitation, not permission to substitute another artifact. Do not regenerate frozen reports: verification is deterministic apart from intentionally retained historical timestamps.
