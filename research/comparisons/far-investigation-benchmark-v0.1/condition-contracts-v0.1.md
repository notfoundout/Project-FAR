# FAR Investigation Benchmark — Condition Contracts v0.1

Status: PREPARED / exact prompts and provider versions remain to be frozen

## Shared input

Every condition receives exactly the same case prompt, source cutoff, retrieval access, wall-clock ceiling, token ceiling, tool-call ceiling, retry allowance, and output-size ceiling.

All conditions must return a user-facing conclusion plus citations/source identifiers. Hidden chain-of-thought is neither requested nor used as evidence. Only visible outputs and recorded tool traces are scored.

## F — FAR-governed investigation

Required visible artifacts: claim inventory; interpretation/scope statement; evidence-to-claim links; contradicting/qualifying evidence; assumptions/dependencies; material alternatives when applicable; inference audit; uncertainty/Unknowns; falsification conditions; provenance/replay record; bounded conclusion.

The condition may use governed FAR schemas/tools but receives no benchmark reference evidence or adjudication material.

## B0 — direct researched answer

Instructional intent: answer the investigation question accurately using available research tools and cite sources. No mandated decomposition, counterevidence search, argument map, FAR vocabulary, or audit schema.

## B1 — generic deep research

Instructional intent: investigate thoroughly; seek supporting and contradicting evidence; assess source quality; explain uncertainties; cite sources; provide a conclusion. No FAR terminology or FAR artifacts.

## B2 — structured fact-check

Instructional intent: identify factual subclaims; collect supporting and contradicting evidence; assess source reliability and context; distinguish verified, contradicted, misleading, and unresolved elements; issue a bounded conclusion. No FAR terminology, factorization/collision machinery, or FAR schemas.

## Matching rule

Prompts may differ only by the workflow instructions defining the conditions. Case content, evidence cutoff, tools, budgets, and provider/model are matched. Any provider feature that automatically grants one condition additional retrieval, memory, context, or hidden resources is disabled or recorded as a mismatch.

## Freeze requirement

The exact byte strings for system/developer/user prompts, model identifier, provider configuration, tool list, retrieval settings, budgets, and retry policy are hashed and frozen before the first case execution. No prompt is edited after any condition output is observed.
