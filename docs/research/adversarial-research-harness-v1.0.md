# Provider-neutral adversarial research harness v1.0

Status: **Reusable infrastructure; no reasoner vote is proof**

The successor harness implements this governed sequence:

```text
frozen problem and staged evidence
  -> isolated blind reasoners
  -> immutable issue extraction
  -> controlled cross-challenge
  -> counterexample work
  -> disagreement ledger
  -> governed human/proof adjudication
```

The implementation is [`adversarial_research_harness.py`](../../tools/adversarial_research_harness.py).
It accepts provider callables wrapped in explicit `ReasonerLane` isolation manifests rather
than hard-coding a vendor CLI. Isolation, distinct sandbox identities, disabled repository
tools, and absence of declared cross-lane state are validated before repository evidence is
read or provider availability is checked. Every invocation has a
stable identity, request hash, evidence hash, phase, provider, raw output or durable failure,
and optional exact replay parent. First-pass issues are frozen before cross-challenge. Revisions
append to issue history instead of erasing the original.

Evidence paths pass through the campaign firewall before any file is read, prompt is built, or
provider is called. Credential-shaped material is deterministically redacted from the problem
and evidence before prompt construction. Recorded-byte replay selects exact invocation IDs,
verifies each original prompt hash, and reproduces recorded successes or failures without
calling a provider. Controlled re-execution is a separate operation and makes no determinism
claim.

## PR #452 extraction boundary

PR #452's stale research state is not imported or rebased. The successor preserves only the
general-purpose ideas of provider isolation, blind first pass, stable issue history, frozen
evidence, bounded replay, calibration hooks, controlled cross-audit, and disagreement tracking.
It specifically regression-tests the unresolved defects observed on that PR:

- redact/allowlist evidence before provider prompt construction;
- bind replay to exact invocation IDs;
- retain failed invocations;
- validate lane isolation before credential/CLI availability;
- append revisions without leaving superseded issue text falsely current.

## Limitations and failure behavior

The harness does not make providers deterministic or prove them independent. A different
provider may share training data, prompts, infrastructure, or framing despite distinct declared
sandboxes. Model identity may be only partially exposed. `isolation_verified` is an auditable
campaign assertion, not remote-infrastructure attestation.
These limits belong in the campaign capsule. A failed lane, malformed response, or unavailable
provider remains in the ledger. Agreement, majority, confidence, calibration, and replay
stability are evidence about the harness; none is a theorem rule.

The harness does not perform final adjudication automatically. Its adjudication record binds a
named adjudicator to exact frozen issues and explicitly records that no reasoner vote was used
as proof.
