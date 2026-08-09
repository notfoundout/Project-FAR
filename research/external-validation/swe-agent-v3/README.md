# SWE-agent v3 FAR augmentation study

Status: **Research — design only**  
Program ID: `FAR-SWE-V3-001`  
Execution authorized: **No**

This directory registers a new causal experiment. It does not repair, continue, or pool the historical SWE-agent v2 comparison.

The experiment asks whether a frozen Project FAR treatment capsule improves software-engineering task performance when the model, task, repository, tools, environment, budgets, and evaluation are otherwise identical. The confirmatory design uses three mandatory arms:

1. `baseline`: the ordinary agent configuration;
2. `placebo`: an inert capsule matched to the FAR capsule for size, structure, read order, and interaction burden;
3. `far`: the frozen FAR treatment capsule.

Project FAR itself is prohibited as a benchmark task repository. Confirmatory tasks must be external and source-identity sealed before execution. The treatment capsule must not contain task identities, repository-specific facts, gold patches, hidden tests, outcomes, or extra model/tool access.

The historical v2 result remains immutable and separate: one task, two repetitions per SWE-agent release, four budget-limited failures, and no observed resolution difference. Its runs are not prior observations for v3 and may not be pooled.

## Current boundary

This package freezes only the causal question, arm structure, estimands, outcome contract, evidence requirements, capsule constraints, prospective corrections, and fail-closed execution gates. It does not authorize a model call, pilot, benchmark run, confirmatory run, grading, outcome reveal, release, or accepted-theory change.

`failure-arithmetic-amendment-v1.1.json` controls its two registered subjects. `review-closure-amendment-v1.2.json` prospectively controls only the bootstrap-seed authority correction, authoritative task identity and deterministic stratum classification, critical-harm thresholds and repetition-slot arithmetic, launch prerequisites, and shallow-checkout historical-authority consumption described in `AMENDMENT-v1.2.md`. The original historical authority bytes are preserved under `historical-base-83c951/` and are manifest-rooted immutable snapshots, not new evidence.

The frozen bootstrap seed remains bound to its originally committed derivation-input identities; later launch-preparation changes cannot rewrite it.

Future instantiated task manifests must use a separate `task_identity_sha256` derived only from provider-stable repository identity, exact repository commit, and sealed task-payload identity. Strata are excluded from that identity, so relabeling cannot turn one underlying task into multiple tasks. `task_identity_sha256` must be unique across the frozen manifest.

Task strata are deterministic multi-label classifications, not operator-selected primary labels. The five frozen boolean classification inputs map one-to-one to the five preregistered strata; every true predicate is retained exactly once in canonical order. Every verifiable classification binding commits a canonical relative evidence path, exact retained-byte SHA-256, and exact byte count. Before launch eligibility can be established, the required validator resolves each path relative to the evidence-registry directory without following symlinks and independently recomputes the retained byte count and SHA-256. Source-derived predicates must use source-evidence bindings; the multi-file reference-patch predicate must use a sealed-reference-patch binding. Required-stratum coverage is checked only after these bindings and bytes verify.

The same mandatory preexecution path applies the frozen population contract to the instantiated records: at least 24 unique authoritative tasks, at least five provider-stable repository identities, no repository above one fifth of the population, one-to-one repository-identity/blind-ID mapping, fixed-width unique blind task IDs, and complete required-stratum coverage. A nonempty manifest alone is never launch evidence.

Critical-harm rate comparisons use the identical frozen task × repetition-slot index for FAR and placebo. Allowed infrastructure replacements occupy the same slot and do not enlarge the denominator. Regression-introduction and invalid-run indicators are defined per frozen repetition slot; every frozen slot remains in the arm denominator, including invalid slots. FAR-minus-placebo rate differences use exact reduced-rational arithmetic, and any missing/duplicated/unpaired slot or missing evidence needed for the harm decision triggers `critical_harm`.

All model calls and benchmark execution are currently blocked. A sacrificial pilot may only be separately authorized after every pre-pilot gate and every exact v1.2 pilot prerequisite is satisfied. Confirmatory execution additionally requires the exact v1.2 confirmatory prerequisites plus every remaining base gate. No such authorization currently exists.

## Integrity model

Every governed data, narrative, prospective-amendment, seed-commitment, and immutable historical-authority snapshot artifact is exact-locked in `design-manifest-v1.0.json`. The verifier checks each committed Git blob and the corresponding worktree bytes, then evaluates the critical semantic contracts. Verifier source is deliberately excluded from the governed-artifact manifest to avoid recursive self-hashing; it remains ordinary reviewed code at the exact PR head.

The historical snapshots make primary verification self-contained in a depth-1 checkout. Delegated v1.1 and v1.2 validators are explicitly bound to the caller's active artifact root, so fixture or alternate-checkout validation cannot silently inspect the canonical checkout instead.

## Verification

The current design-only package has no instantiated task population, so the static commands verify contracts and keep execution blocked:

```bash
python research/external-validation/swe-agent-v3/verify_design.py
python research/external-validation/swe-agent-v3/verify_review_closure_v1_2.py
python -m unittest discover -s tests -p 'test_swe_agent_v3*.py' -v
python -m py_compile \
  research/external-validation/swe-agent-v3/verify_integrity.py \
  research/external-validation/swe-agent-v3/verify_design.py \
  research/external-validation/swe-agent-v3/verify_review_closure.py \
  research/external-validation/swe-agent-v3/verify_review_closure_v1_2.py \
  tests/test_swe_agent_v3*.py
```

Before any pilot or confirmatory launch can be considered eligible, the frozen instantiated manifest and its evidence registry must additionally pass the required CLI path together:

```bash
python research/external-validation/swe-agent-v3/verify_review_closure_v1_2.py \
  --task-manifest /path/to/frozen-task-manifest.json \
  --evidence-registry /path/to/frozen-evidence-registry.json
```

Supplying only one of those artifacts is invalid. If the execution gate ever claims pilot or confirmatory authorization, the no-argument static CLI fails rather than reporting launch eligibility without inspecting instantiated records and retained evidence.
