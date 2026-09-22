# FAR Investigation Benchmark — Condition Contracts v0.1

Status: PREPARED / exact prompts and provider versions remain to be frozen

## Shared input

Every condition receives exactly the same case prompt, source cutoff, retrieval access, wall-clock ceiling, token ceiling, tool-call ceiling, retry allowance, and output-size ceiling.

All conditions must return a user-facing conclusion plus citations/source identifiers. Hidden chain-of-thought is neither requested nor used as evidence. Only visible outputs and recorded tool traces are scored.

## F — FAR-governed investigation

Condition F must execute the canonical FAR workflow in \`frameworks/FAR/workflow.md\`, including the Contract-Discovery Intake Gate whenever the raw case does not itself supply a schema-valid downstream comparison contract. It must freeze the resulting comparison contract/family before substantive evaluation, preserve typed Unknown boundaries, construct and charge the representation, and run the contract-relative factorization audit: decoder/factorization evidence where sufficiency is established, collision evidence where refuted, or OPEN when neither is established. Any canonical stage not applicable must be explicitly marked NOT APPLICABLE with a reason.

Required visible artifacts include the governed intake/freeze identity, claim inventory, interpretation/scope statement, comparison contract or family, evidence-to-claim links, contradicting/qualifying evidence, assumptions/dependencies, material alternatives, representation/machinery record, factorization/collision/OPEN disposition, inference audit, uncertainty/Unknowns, falsification conditions, provenance/replay record, and typed bounded conclusion.

The condition uses the governed FAR schemas/tools required by the canonical workflow but receives no benchmark reference evidence or adjudication material.

## B0 — direct researched answer

Instructional intent: answer the investigation question accurately using available research tools and cite sources. No mandated decomposition, counterevidence search, argument map, FAR vocabulary, or audit schema.

## B1 — generic deep research

Instructional intent: investigate thoroughly; seek supporting and contradicting evidence; assess source quality; explain uncertainties; cite sources; provide a conclusion. No FAR terminology or FAR artifacts.

## B2 — structured fact-check

Instructional intent: identify factual subclaims; collect supporting and contradicting evidence; assess source reliability and context; distinguish verified, contradicted, misleading, and unresolved elements; issue a bounded conclusion. No FAR terminology, factorization/collision machinery, or FAR schemas.

## Matching rule

Prompts may differ only by the workflow instructions defining the conditions. Case content, evidence cutoff, tools, budgets, and provider/model are matched. Any provider feature that automatically grants one condition additional retrieval, memory, context, or hidden resources is disabled or recorded as a mismatch.

## Freeze requirement

The exact byte strings for system/developer/user prompts, model identifier, provider configuration, tool list, retrieval settings, budgets, retry policy, **execution schedule**, and session-isolation policy are hashed and frozen before the first case execution. No prompt is edited after any condition output is observed.

## Execution order and isolation

There are 60 case blocks and four conditions per block. For each case, derive a deterministic condition order by sorting F/B0/B1/B2 on \`SHA256("20260922-execution-order" || case_id || condition_id)\` using UTF-8 and literal ASCII \`||\` separators. Execute cases in ascending case ID. Each case-condition run starts in a fresh provider session with no shared conversation state, cache priming, hidden intermediate artifact, or cross-condition memory. If provider-side cache isolation cannot be guaranteed, record that limitation and use unique neutral run nonces across **all** conditions so no condition systematically benefits from earlier cache state. The frozen schedule is emitted before execution and cannot be reordered after outputs are observed.
