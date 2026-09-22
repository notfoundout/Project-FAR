# FAR Investigation Benchmark — Condition Contracts v0.1

Status: PREPARED / exact prompt bytes and provider snapshot remain to be frozen

## Shared input

Every condition receives exactly the same case prompt, source cutoff, retrieval access, wall-clock ceiling, output-token ceiling, retrieval/tool-call ceiling, retry allowance, and output-size ceiling.

All conditions return a user-facing conclusion plus citations/source identifiers. Hidden chain-of-thought is neither requested nor used as evidence. Only visible outputs and recorded tool traces are scored.

## Shared model and tool identity

Within every case block, all four conditions use the same immutable model identifier/provider snapshot and the same provider settings. If the provider exposes only a rolling alias, `environment-lock.json` records the alias, all available version/fingerprint metadata, request configuration, and the limitation. A detected provider/model/tool drift outside the frozen tolerance makes the affected comparison an integrity mismatch.

Retrieval tools, search settings, locale/language settings, account/session capabilities, memory, connectors, and any provider feature that can change available evidence are matched and frozen. Features that cannot be matched are disabled where possible and otherwise declared before S1.

## Shared source cutoff

All evidence used by a condition must satisfy the frozen source cutoff. For mutable living pages, the materially relied-on content must be reproducibly attributable to a version that existed by the cutoff. A later page version is inadmissible unless an archived/versioned snapshot establishes the pre-cutoff content.

## F — FAR-governed investigation

Condition F must execute the canonical FAR workflow in `frameworks/FAR/workflow.md`, including the Contract-Discovery Intake Gate whenever the raw case does not itself supply a schema-valid downstream comparison contract. It freezes the resulting comparison contract/family before substantive evaluation, preserves typed Unknown boundaries, constructs and charges the representation, and runs the contract-relative factorization audit: decoder/factorization evidence where sufficiency is established, collision evidence where refuted, or OPEN when neither is established. Any canonical stage not applicable is explicitly marked NOT APPLICABLE with a reason.

Required visible artifacts include the governed intake/freeze identity, claim inventory, interpretation/scope statement, comparison contract or family, evidence-to-claim links, contradicting/qualifying evidence, assumptions/dependencies, material alternatives, representation/machinery record, factorization/collision/OPEN disposition, inference audit, uncertainty/Unknowns, falsification conditions, provenance/replay record, and typed bounded conclusion.

The condition uses the governed FAR schemas/tools required by the canonical workflow but receives no benchmark reference evidence or adjudication material.

## B0 — direct researched answer

Instructional intent: answer the investigation question accurately using available research tools and cite sources. No mandated decomposition, counterevidence search, argument map, FAR vocabulary, or audit schema.

## B1 — generic deep research

Instructional intent: investigate thoroughly; seek supporting and contradicting evidence; assess source quality; explain uncertainties; cite sources; provide a conclusion. No FAR terminology or FAR artifacts.

## B2 — structured fact-check

Instructional intent: identify factual subclaims; collect supporting and contradicting evidence; assess source reliability and context; distinguish verified, contradicted, misleading, and unresolved elements; issue a bounded conclusion. No FAR terminology, factorization/collision machinery, or FAR schemas.

## Prompt-byte freeze

`condition-prompts.json` is the sole frozen source for the condition-specific instruction bytes. It defines exactly F/B0/B1/B2. For each condition, the system, developer, and user-template surfaces are either `null` or an object containing exact base64 bytes plus SHA-256. Every user template contains exactly one literal `{{CASE_PROMPT}}` marker.

For a run, render only by replacing the marker with the exact UTF-8 `case_prompt` bytes bound in `cases.jsonl`. No other normalization, templating, date insertion, hidden instruction, or per-case editing is permitted.

## Matching rule

Prompts may differ only by the frozen workflow instructions defining the conditions. Case content, evidence cutoff, model/provider snapshot, tools, budgets, provider settings, and execution environment are matched. Any automatically granted condition-specific retrieval, memory, context, or hidden resource is disabled or recorded as an integrity mismatch under the frozen rule.

## Freeze requirement

The exact prompt bytes, model/provider snapshot, provider configuration, tool list, retrieval settings, source cutoff, budgets, retry policy, execution schedule, and session-isolation policy are hashed and frozen before the first condition run. No condition prompt or runtime setting is edited after S1 begins.

## Execution order and isolation

There are exactly 60 case blocks and four conditions per block. Final case IDs are fixed by the case-selection protocol. For each case, derive condition order by sorting F/B0/B1/B2 lexicographically on the lowercase hexadecimal digest:

`SHA256(UTF8("20260922-execution-order|" + case_id + "|" + condition_id))`

Ties are impossible unless condition IDs are equal. Execute case blocks in ascending `case_id`. `execution-schedule.json` materializes all 240 ordered runs with stable run IDs before S1 and is hashed into the frozen campaign.

Each case-condition run starts in a fresh provider session with no shared conversation state, cache priming, hidden intermediate artifact, or cross-condition memory. If provider-side cache isolation cannot be guaranteed, record that limitation and use unique neutral run nonces across **all** conditions so no condition systematically benefits from earlier cache state. The nonce may identify a run but must not encode condition semantics or expected outcome.

The frozen schedule cannot be reordered, inserted into, or truncated after any condition output exists except where infrastructure failure triggers the frozen retry policy for the same stable run ID. Every retry and reason is retained.
