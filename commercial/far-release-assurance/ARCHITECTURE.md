# FAR Release Assurance — Commercial Architecture v0.1

## 1. Product boundary

FAR Release Assurance compares a baseline AI-agent release with a candidate release and produces auditable evidence for one of four outcomes: `Pass`, `Review required`, `Blocked`, or `Unknown`.

The product reconstructs and validates disclosed and instrumented decision dependencies. It does not read hidden chain of thought, prove safety, establish complete causal truth from incomplete telemetry, or certify legal compliance.

The commercial layer must remain distinct from Project FAR's research theorem, FARA, FARE, FARM, UPP, and PTE. Research artifacts may constrain definitions and tests; commercial telemetry cannot upgrade research evidence.

## 2. First framework and deployment choice

The first supported target is a custom Python reference agent using OpenTelemetry-compatible JSON spans. This choice minimizes framework-specific assumptions while retaining a direct path to OpenInference and OpenAI Agents SDK adapters.

Initial execution modes:

1. local CLI;
2. GitHub Actions gate;
3. service-assisted audit using the same local evidence package.

No dashboard is required for the first milestone.

## 3. System architecture

```text
Git repository + release refs + manifests + traces + policies
                            |
                            v
                   Source collectors
                            |
                            v
                  FAR normalization layer
                            |
                            v
       Release manifest + machinery inventory + event ledger
                            |
                            v
        Commitment/dependency evidence graph per release
                            |
                            v
 Machinery closure + replay assessment + release comparison
                            |
                            v
       Findings ledger + deterministic decision adjudicator
                            |
                            v
 Markdown report + JSON evidence package + CI exit status
```

### Components

- `collect.git`: resolves commits and changed files without inferring runtime use from source presence alone.
- `collect.trace`: ingests versioned OpenTelemetry/OpenInference-compatible spans.
- `collect.manifest`: ingests prompts, tools, models, policies, stores, environment, and memory declarations.
- `normalize`: converts source-specific records into FAR commercial events and machinery nodes.
- `graph`: constructs commitment, evidence, dependency, revision, identity, and machinery edges.
- `closure`: performs deterministic cycle-safe fixed-point traversal from declared decision and release roots.
- `compare`: computes baseline/candidate deltas and integrity regressions.
- `rules`: evaluates explicit findings without silently resolving missing information.
- `report`: emits stable Markdown and JSON artifacts with hashes.

## 4. Minimal event schema

Every normalized event contains:

- `event_id`: stable identifier within the run;
- `run_id`, `release_id`, `sequence`;
- `event_type`;
- `subject_id` and optional `object_ids`;
- `evidence_refs` and `dependency_refs`;
- `machinery_refs`;
- `identity_context`;
- `status`;
- `source_ref` with trace/span/file provenance;
- `timestamp` when supplied, never synthesized as causal order;
- `attributes` for adapter-specific data.

Required event types:

- `commitment_introduced`;
- `evidence_attached`;
- `dependency_declared`;
- `constraint_applied`;
- `action_selected`;
- `conclusion_derived`;
- `support_invalidated`;
- `commitment_revised`;
- `commitment_withdrawn`;
- `identity_changed`;
- `identity_revalidated`;
- `state_externalized`;
- `unknown_recorded`.

## 5. Minimal machinery schema

Each machinery item contains:

- stable `machinery_id`;
- `kind`;
- declared name and version/digest;
- release applicability;
- source and provenance;
- required dependencies;
- declaration status;
- evidence status;
- effectiveness status;
- validation status;
- mutability and externality;
- secret-redacted configuration digest;
- optional replay material reference.

Initial machinery kinds:

`prompt`, `model`, `tool`, `api`, `policy`, `runtime`, `configuration`, `scheduler`, `randomness_source`, `database`, `vector_store`, `memory_store`, `external_state_store`, `identity_registry`, `codebook`, `decoder`, `interpreter`, `learned_artifact`, `fine_tune`, `human_approval`, `evaluation_dataset`, `benchmark`, `other`.

Evidence status is one of:

`confirmed`, `inferred`, `disclosed_unverified`, `missing`, `contradictory`, `ineffective`, `invalid`, `unknown`.

## 6. Machinery closure specification

Inputs:

- release roots;
- decision roots;
- declared machinery graph;
- observed machinery references;
- validation and effectiveness evidence.

Algorithm:

1. Canonically sort roots.
2. Traverse required dependencies using a work queue and visited set.
3. Preserve duplicate identifiers as defects rather than coalescing them silently.
4. Record undeclared observed nodes and declared-but-unreached nodes separately.
5. Terminate when the queue is empty.
6. Re-running over identical canonical inputs must produce identical ordered output.

Outcome:

- `Closed`: every transitively required item is disclosed, present, effective, valid, and reached.
- `Open`: at least one required item is absent, concealed, ineffective, invalid, contradictory, or unsupported.
- `Unknown`: no opening defect is established, but at least one required item remains unresolved.

Required properties:

- finite termination over finite manifests;
- cycle safety;
- idempotence;
- deterministic ordering;
- monotonic improvement when effective valid support is added, except when the addition reveals a new required dependency;
- explicit duplicate-identity and undeclared-root findings.

## 7. Baseline-versus-candidate comparison specification

Comparison is performed over canonical release packages, never raw unordered traces.

Comparison dimensions:

1. release identity and source commit;
2. machinery additions, removals, version changes, mutability changes, and newly unresolved items;
3. decision-dependency graph changes;
4. evidence-source and evidence-status changes;
5. policy and constraint changes;
6. invalidation propagation;
7. revision and withdrawal behavior;
8. identity continuity and revalidation;
9. external-state reliance;
10. replay completeness and deterministic reproduction;
11. evaluation-data and benchmark dependency changes;
12. output metrics, reported separately from reasoning integrity.

A material regression exists when the candidate introduces or worsens a condition that can alter authorization, identity, support validity, policy application, reproducibility, or the evidence available to justify a consequential action.

Output equality never cancels a reasoning-integrity defect.

## 8. Finding model

Each finding contains:

- `finding_id`;
- `rule_id` and version;
- severity: `info`, `low`, `medium`, `high`, `critical`;
- disposition: `confirmed`, `inferred`, `unknown`, `dismissed`;
- baseline evidence refs;
- candidate evidence refs;
- affected commitments, machinery, runs, policies, and identities;
- rationale;
- remediation;
- deterministic fingerprint.

Core MVP rules:

- unversioned or mutable policy introduced;
- undeclared observed machinery;
- required machinery missing or unresolved;
- invalidated support not propagated to dependent active commitments;
- identity changed without revalidation before consequential action;
- replay depends on undisclosed memory or external state;
- benchmark/evaluation information enters operational machinery;
- duplicate machinery identity;
- candidate replay completeness materially decreases;
- candidate output metric improves while a high-severity integrity regression occurs.

## 9. Decision specification

Decision priority is `Blocked` > `Review required` > `Unknown` > `Pass`.

### Blocked

Return `Blocked` when at least one confirmed high/critical finding violates a configured blocking rule, including:

- unauthorized data or policy dependency;
- active conclusion retained after confirmed sole-support invalidation;
- unvalidated identity drift before consequential action;
- confirmed benchmark leakage;
- confirmed hidden required machinery;
- replay or closure defect that makes the release evidence package materially misleading.

### Review required

Return `Review required` when:

- a confirmed medium finding requires human risk acceptance;
- an inferred high/critical finding has sufficient evidence to prevent automatic passage but not enough for `Blocked`;
- the candidate changes consequential policy, model, tool, identity, or external-state dependencies without a pre-authorized rule.

### Unknown

Return `Unknown` when:

- no block or mandatory review is established;
- unresolved required machinery, missing traces, contradictory telemetry, or incomplete replay evidence prevents a justified pass.

`Unknown` is not a weaker pass and must produce a nonzero CI gate status unless policy explicitly permits advisory mode.

### Pass

Return `Pass` only when:

- no blocking or review finding applies;
- required machinery closure is `Closed` for configured roots;
- required trace and replay thresholds are met;
- no unresolved fact is material to the configured release policy.

## 10. CLI contract

```text
far-release init [--path PATH]
far-release ingest --repo PATH --release ID --ref GIT_REF --manifest FILE --traces PATH
far-release inventory --release ID [--json FILE]
far-release compare --baseline ID --candidate ID [--policy FILE]
far-release gate --comparison FILE [--mode enforce|advisory]
far-release report --comparison FILE --format markdown|json --output PATH
far-release verify-package PATH
```

Exit codes:

- `0`: Pass;
- `2`: Review required;
- `3`: Blocked;
- `4`: Unknown;
- `10`: invalid input or schema;
- `11`: internal deterministic-processing failure.

## 11. Repository layout

```text
commercial/far-release-assurance/
  ARCHITECTURE.md
  README.md
  schemas/
    release-package.schema.json
    release-report.schema.json
  src/far_release_assurance/
    model.py
    closure.py
    compare.py
    decision.py
    report.py
    cli.py
    adapters/
      reference_python.py
      otel_json.py
  examples/reference-agent/
  examples/adversarial/
  tests/
  .github/workflows/far-release-assurance.yml
```

The prototype remains a separate package. It may import stable mechanization primitives through an explicit adapter, but it must not redefine or mutate research artifacts.

## 12. Reference agent application

The reference agent is a deterministic customer-support eligibility agent with:

- versioned customer identity record;
- versioned refund policy;
- one customer-data tool;
- one policy lookup tool;
- optional memory store;
- explicit commitments and evidence references;
- a handoff event;
- JSON trace output.

It must support baseline and candidate configurations for every adversarial scenario.

## 13. Adversarial demonstrations

1. **Unauthorized dependency**: candidate reads an unapproved customer-data source; output remains correct.
2. **Stale policy**: candidate replaces `policy-v4.json` with mutable remote content returning the same current text.
3. **Invalidated support**: customer eligibility evidence is withdrawn, but the refund approval remains active.
4. **Hidden memory**: replay succeeds only with an undeclared local memory database.
5. **Identity drift**: handoff changes `customer_id` and no revalidation occurs before approval.
6. **Benchmark leakage**: candidate gains access to expected evaluation labels through a hidden tool or memory namespace.
7. **Same output, different integrity**: candidate produces identical answers using unresolved external state.

Each demonstration must include conventional output assertions that pass and FAR assertions that fail.

## 14. GitHub Actions workflow design

The CI job must:

1. check out full history;
2. install the isolated commercial package;
3. validate schemas and policy;
4. ingest baseline artifacts from a trusted artifact, commit, or explicit fixture;
5. ingest candidate artifacts from the checked-out commit;
6. compare releases;
7. emit Markdown and JSON reports;
8. upload the evidence package;
9. set the job result from the decision exit code;
10. print the report hash and retain the exact policy version.

No CI success may be described as proof of the research theorem or independent review.

## 15. Sample report

```text
FAR Release Assurance: BLOCKED
Baseline: 396eedc
Candidate: 13a1659
Policy: release-policy/0.1

Material findings
- CRITICAL: Candidate moved from policy-v4 to an unversioned remote policy source.
- CRITICAL: Customer identity changed during handoff and was not revalidated.
- HIGH: Seven active conclusions retained invalidated sole support.
- HIGH: Four transitively required external dependencies remain unresolved.

Machinery closure: OPEN
Replay completeness: 81%
Output accuracy: 82% -> 87%
Reasoning-integrity disposition: regressed

Decision basis
The accuracy improvement does not offset confirmed authorization, identity, support-propagation, and closure defects.
```

## 16. Directly reusable Project FAR components

Reusable through versioned adapters:

- canonical identifier and reference concepts;
- typed claims, evidence, operations, reasoning steps, and dependencies;
- graph node and edge structures;
- deterministic normalization and serialization patterns;
- duplicate identifier validation;
- diagnostics and source-location patterns;
- explicit `Unknown` discipline;
- machinery-closure definitions and executable invariants where implementation contracts match;
- immutable result and evidence-ledger practices;
- claim-impact separation patterns;
- adversarial test style and deterministic checkers.

Reuse requires commercial applicability tests. Research naming alone does not establish product fitness.

## 17. Research artifacts that remain separate

Do not import as commercial conclusions or mutate from commercial code:

- terminal theorem statements and proofs;
- FARA as a privileged architecture;
- FARE foundation governance;
- FARM program coordination state;
- UPP and PTE result registries;
- independent-review eligibility or review records;
- research claim-status dashboards;
- empirical universality claims;
- proof-assistant evidence labels;
- research workstream adjudications.

Commercial findings may cite a versioned technical rule derived from research, but cannot alter research evidence status.

## 18. Thirty-day backlog ordered by dependency

### Days 1–5: contracts

1. Freeze release-package, report, event, machinery, and finding schemas.
2. Freeze decision-policy v0.1 and exit-code contract.
3. Implement canonical serialization and content hashing.
4. Build fixture validator and schema tests.

### Days 6–10: ingestion and inventory

5. Implement Git release manifest collector.
6. Implement OpenTelemetry JSON trace adapter.
7. Implement reference-agent trace emitter.
8. Implement machinery inventory and undeclared-observation detection.

### Days 11–15: graph and closure

9. Implement event-to-graph normalization.
10. Implement cycle-safe fixed-point machinery closure.
11. Add duplicate identity, undeclared root, open, and unknown tests.
12. Emit canonical dependency graph JSON.

### Days 16–20: comparison and rules

13. Implement baseline/candidate machinery and graph diff.
14. Implement support invalidation propagation.
15. Implement identity continuity/revalidation rule.
16. Implement replay completeness and hidden-memory rules.
17. Implement benchmark-leakage rule.

### Days 21–25: adjudication and reports

18. Implement deterministic decision engine.
19. Implement Markdown and JSON report generation.
20. Implement immutable report hashing and package verification.
21. Implement CLI and exit codes.

### Days 26–30: demonstrations and CI

22. Build seven adversarial fixtures with passing output tests.
23. Add regression and mutation tests.
24. Add GitHub Actions gate and artifact upload.
25. Run the complete reference demonstration.
26. Produce the first service-assisted audit template.
27. Freeze v0.1 known limitations and threat model.

## 19. Assumptions, Unknowns, and commercial risks

### Assumptions

- customers can provide versioned traces, manifests, and release refs;
- at least one consequential decision can be mapped to explicit roots;
- source and trace identifiers can be normalized without exposing secrets;
- engineering teams accept a non-pass result when evidence is incomplete.

### Unknowns

- minimum telemetry completeness required for useful decisions in real customer systems;
- adapter effort across agent frameworks;
- acceptable false-positive rate for inferred dependencies;
- buyer and budget owner;
- willingness to disclose prompts, memory, and external services;
- whether customers will permit local-only audits but reject hosted processing;
- which rules generalize beyond the reference agent without excessive configuration.

### Risks

- overclaiming hidden-cognition reconstruction;
- becoming a tracing dashboard with extra labels;
- weak provenance allowing fabricated or stale evidence packages;
- rule proliferation that makes outcomes non-explainable;
- conflating missing telemetry with confirmed defects;
- exposing customer secrets in reports;
- coupling commercial releases to mutable research code;
- premature open-sourcing of distinctive adjudication logic;
- selling compliance language unsupported by the product;
- insufficient proof that findings change release decisions.

## 20. First milestone acceptance test

The milestone passes only when all of the following are true:

1. baseline and candidate output tests both pass;
2. candidate introduces one material adversarial defect;
3. FAR produces a deterministic non-pass outcome with exact evidence references;
4. a technically competent reviewer can reproduce the result from the evidence package;
5. the finding is clear enough to justify changing or blocking the release;
6. no report language upgrades the Project FAR theorem or claims access to hidden cognition.
