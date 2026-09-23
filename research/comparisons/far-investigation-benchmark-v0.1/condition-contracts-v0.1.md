# FAR Investigation Benchmark — Condition Contracts v0.1

Status: PREPARED / exact prompt bytes and provider snapshot remain to be frozen

## Shared input

Every condition receives exactly the same case prompt, source cutoff, retrieval access, wall-clock ceiling, output-token ceiling, retrieval/tool-call ceiling, retry allowance, and output-size ceiling.

All conditions return a user-facing conclusion plus citations/source identifiers. Hidden chain-of-thought is neither requested nor used as evidence. Only visible outputs and recorded tool traces are scored.

## Shared model and tool identity

Every one of the 240 runs uses the same immutable model identifier/provider snapshot and the same provider settings unless the frozen environment contract explicitly records a provider limitation that cannot expose an immutable identifier. If the provider exposes only a rolling alias, `environment-lock.json` records the alias, all available version/fingerprint metadata, request configuration, and the limitation. A detected provider/model/tool drift outside the frozen tolerance is an integrity mismatch rather than an unrecorded substitution.

Retrieval tools, search settings, locale/language settings, account/session capabilities, memory, connectors, and any provider feature that can change available evidence are matched and frozen. Features that cannot be matched are disabled where possible and otherwise declared before S1.

## Shared source cutoff

All evidence used by a condition must satisfy the frozen source cutoff. For mutable living pages, materially relied-on content must be reproducibly attributable to a version that existed by the cutoff. A later page version is inadmissible unless an archived/versioned snapshot establishes the pre-cutoff content.

## F — FAR-governed investigation

Condition F must execute the canonical FAR workflow in `frameworks/FAR/workflow.md`, including the Contract-Discovery Intake Gate whenever the raw case does not itself supply a schema-valid downstream comparison contract. It freezes the resulting comparison contract/family before substantive evaluation, preserves typed Unknown boundaries, constructs and charges the representation, and runs the contract-relative factorization audit: decoder/factorization evidence where sufficiency is established, collision evidence where refuted, or OPEN when neither is established. Any canonical stage not applicable is explicitly marked NOT APPLICABLE with a reason.

Required visible artifacts include the governed intake/freeze identity, claim inventory, interpretation/scope statement, comparison contract or family, evidence-to-claim links, contradicting/qualifying evidence, assumptions/dependencies, material alternatives, representation/machinery record, factorization/collision/OPEN disposition, inference audit, uncertainty/Unknowns, falsification conditions, provenance/replay record, and typed bounded conclusion.

The complete transitive treatment-defining source set is frozen through `far-treatment-source-manifest.json`, including the canonical FAR workflow, contract-discovery and methodology-audit protocols, intake schema, and FARA architectural dependencies required by the workflow. Condition F receives no benchmark reference evidence or adjudication material.

## B0 — direct researched answer

Instructional intent: answer the investigation question accurately using available research tools and cite sources. No mandated decomposition, counterevidence search, argument map, FAR vocabulary, or audit schema.

## B1 — generic deep research

Instructional intent: investigate thoroughly; seek supporting and contradicting evidence; assess source quality; explain uncertainties; cite sources; provide a conclusion. No FAR terminology or FAR artifacts.

## B2 — structured fact-check

Instructional intent: identify factual subclaims; collect supporting and contradicting evidence; assess source reliability and context; distinguish verified, contradicted, misleading, and unresolved elements; issue a bounded conclusion. No FAR terminology, factorization/collision machinery, or FAR schemas.

## Prompt-byte freeze

`condition-prompts.json` is the sole frozen source for condition-specific instruction bytes. It defines exactly F/B0/B1/B2. For each condition, the system, developer, and user-template surfaces are either `null` or an object containing exact base64 bytes plus SHA-256. Every user template contains exactly one literal `{{CASE_PROMPT}}` marker.

For a run, render only by replacing that marker with the exact UTF-8 `case_prompt` bytes bound in `cases.jsonl`. No other normalization, templating, date insertion, nonce insertion, hidden instruction, or per-case editing is permitted.

## Matching rule

Prompts may differ only by the frozen workflow instructions defining the conditions. Case content, evidence cutoff, model/provider snapshot, tools, budgets, provider settings, and execution environment are matched. Any automatically granted condition-specific retrieval, memory, context, or hidden resource is disabled or recorded as an integrity mismatch under the frozen rule.

## Freeze requirement

The exact prompt bytes, model/provider snapshot, provider configuration, tool list, retrieval settings, source cutoff, budgets, retry policy, execution schedule, cache/session-isolation mechanism, adjudication presentation schedule, and treatment-source bindings are hashed and frozen before the first condition run. No condition prompt or runtime setting is edited after S1 begins.

## Execution order

`execution-schedule.json` contains exactly one run for every Cartesian product of the 60 final case IDs and conditions F/B0/B1/B2, exactly 240 runs total.

For every case-condition pair, compute:

`SHA256(UTF8("20260922|schedule|" + case_id + "|" + condition_id))`

Sort all 240 pairs globally by the lowercase hexadecimal digest and assign `execution_index = 1..240`. `execution-schedule.json` stores each `case_id`, condition, stable `run_id`, digest as `schedule_key`, execution index, and the frozen cache nonce defined below. No case-block ordering or alternate per-case permutation is permitted.

The frozen schedule cannot be reordered, inserted into, or truncated after any condition output exists except where infrastructure failure triggers the frozen retry policy for the same stable `run_id`. Every retry and reason is retained.

## Session and cache isolation

Each case-condition run starts in a fresh provider session with no shared conversation state, hidden intermediate artifact, or cross-condition memory.

Shared model-visible cache state is forbidden. Before S1, `environment-lock.json` must establish one of exactly two mechanisms for every run:

1. `provider_isolated_context`: a provider-documented isolated/no-shared-cache context; or
2. `non_model_visible_nonce`: a provider metadata/header channel that is not model-visible and does not consume the model-visible token budget.

For the nonce mechanism, the exact nonce for a run is:

`SHA256(UTF8("FAR-INVESTIGATION-BENCHMARK-0.1|cache|" + run_id))`

The nonce is transported only through the frozen non-model-visible provider channel recorded in `environment-lock.json`. It must never appear in system, developer, user, retrieval query, tool-call content, or any other model-visible bytes. If neither isolation mechanism is available for every condition, the campaign is BLOCKED before S1 rather than modifying prompts to simulate isolation.

## Resource ceilings

Reaching a frozen wall-clock, token, retrieval/tool-call, retry, or output-size ceiling is part of the observed benchmark outcome. A ceiling hit is not an exclusion and does not permit a replacement run with more resources.

Only an exogenous infrastructure/configuration failure that prevents execution of the frozen condition as specified may make the entire four-condition case non-ratable under the frozen missingness rule. That classification must be condition-blind and documented; no post-S1 case replacement is permitted.
