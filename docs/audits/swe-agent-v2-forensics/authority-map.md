# SWE-agent v2 authority map

Status: **Research; derived analysis**

| Class | Canonical authority | Role / boundary |
|---|---|---|
| Frozen evidence | [`commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/`](../../../commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/) | Outcome-blind immutable packages, adjudication, locks. |
| Frozen reveal/reports | [`commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/`](../../../commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/) | Authoritative mapping, grader summaries, 0/2 counts, bounded conclusion and decision. Never regenerated here. |
| External source evidence | `execution-output/` members enumerated in `primary-freeze/source-artifact-lock.json` | Authoritative-by-hash but content absent from Git; insufficient for exact forensic chronology. |
| Protocol/configuration | `PREREGISTRATION.md`, `manifest.json`, `agent-config.yaml`, environment/access/shared locks | Declared design and identities, not proof of runtime success. |
| Implementation | v2 Python files in the case directory | Producer logic, not outcome evidence. |
| Orchestration | `.github/workflows/far-swe-agent-*-v2.yml` | Workflow mechanics; outer conclusion is not inner success. |
| Validation | v2 tests, `verify_reveal_hardened.py`, `tools/check_post_swe_agent_v2_stabilization.py` | Integrity checks; do not prove patch correctness. |
| Documentation | status, reproducibility, governance registers, stabilization audit | Current interpretive boundaries. |
| Derived forensic analysis | this directory | Non-frozen reconstruction with provenance and explicit uncertainty. |
| Historical material | predecessor v1 case and earlier Gemini 2.5/free-tier episode | Context only; not pooled with frozen comparison. |

Architecture, terminology, framework boundaries and dependency authority were inspected in `docs/ARCHITECTURE.md`, `docs/CANONICAL_MAP.md`, `docs/governance/*`, `docs/project-status.md`, `docs/ROADMAP.md`, `docs/DECISION_LOG.md`, the stabilization audit, reproducibility guide, workflow definitions, validators and report generators. The final report outranks derived analysis for recorded outcomes.
