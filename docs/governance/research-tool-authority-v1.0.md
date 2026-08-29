# Project FAR research-tool authority v1.0

Status: **Accepted operational governance; no theory change**

Machine source: [`research-tools-v1.0.json`](../../research/registry/research-tools-v1.0.json).

## Authority rule

The GitHub repository's governed `main` state is the sole canonical Project FAR state. A tool
may help discover, calculate, prove relative to an encoding, review, implement, organize, or
display. It may not acquire authority merely because it is sophisticated, external, popular,
or agrees with another tool.

| Tool class | Legitimate output | Authority boundary |
|---|---|---|
| GitHub | versioned source, governance, evidence, review, and history | canonical Project FAR state; merge/CI is not mathematical proof |
| Lean | kernel-checked derivation relative to exact encoded premises | encoding/alignment and theorem scope require separate audit |
| Wolfram and computational systems | bounded checks, symbolic calculations, candidate counterexamples | no unrestricted proof; finite agreement never proves universality |
| Consensus, SciSpace, Scite, Acumen/Talarion, ordinary web research | source and prior-art discovery, citation contexts, query records | discover evidence; never govern FAR, prove novelty, or close claims |
| Zotero | bibliographic identity, deduplication, keys, collections, attachments, exports | controls bibliography workflow, not theorem, claim, or novelty status |
| GPT/OpenAI, Claude, and other reasoners | replaceable implementation, reconstruction, critique, counterexample, and review lanes | never intrinsic closure authorities; votes and agreement are not proof |
| Notion and Linear | optional notes, meeting, planning, and task mirrors | noncanonical; GitHub wins every conflict |
| Base44 and Floot | noncanonical prototypes and usability experiments | may implement a pinned interface; may not redefine FAR semantics |
| OpenAI Agents SDK and ChatGPT Apps/MCP | agent orchestration and application transport | must expose version, scope, provenance, and repository-derived authority |

## Proof and computation

Lean establishes that a declaration follows under the encoded types, definitions, imports,
axioms, and logic. It does not establish that the encoding faithfully matches a governing
prose statement. Every promoted declaration therefore needs a source hash/location, explicit
assumptions, an alignment test, and premise-sensitivity controls.

Wolfram, finite enumeration, model checking, CI, repository consistency, and reference-model
agreement are checks or counterexample mechanisms. They do not become unrestricted proof
authority. A valid computational counterexample under exact premises can refute a theorem; a
failed search cannot prove its absence.

## Research and citation systems

Research systems may discover candidate evidence and prior art. Queries, dates, result sets,
rejection reasons, and the admitted corpus must be retained when a campaign depends on them.
Negative search results never certify novelty or priority. Primary sources should be checked
where available, and a source's bibliographic identity must remain distinct from the
Project-FAR judgment about what it supports, disputes, contextualizes, anticipates, or fails to
establish.

Zotero may own local collection organization and stable citation keys. GitHub owns the
claim-to-source, artifact, scope, prior-art, and support/dispute/context relationships. A
Zotero item or citation does not alter theorem status.

## Models and external reasoners

Models are replaceable reasoners and reviewers. A different provider does not by itself create
independence. The record must disclose, as far as available: model identity, prior exposure,
shared prompts or corpora, tool access, memory/state sharing, conflicts, freeze times, failures,
and controlled unblinding.

Blind lanes must receive redacted/allowlisted evidence **before** prompt construction. First
passes are frozen before cross-audit. Cross-challenge is controlled and preserves the original
issue history. Failed invocations remain evidence. No majority, unanimity, confidence score,
or provider diversity is a proof rule.

## Contamination controls

A consequential campaign must use a staged access manifest where feasible. Each stage records
allowed and prohibited paths/sources, exposure receipts, prompt/protocol versions, and hashes.
The firewall validator fails closed on absolute paths, parent traversal, denylisted content,
or paths outside the allowlist. Unblinding creates a new stage; it never mutates the frozen
blind record.

If an evaluator has material prior exposure, that exposure is reported and the evidence is
classified accordingly. Tool-generated summaries must not be inserted into a supposedly
clean-room prompt unless the manifest admits them. Provider credentials, workspaces, and
state are isolated where feasible; limitations are recorded where perfect isolation or
deterministic replay is impossible.

## Mirrors, prototypes, and applications

Notion and Linear may mirror or support work but never resolve a conflict against GitHub.
Base44, Floot, Agents SDK, and ChatGPT Apps/MCP may implement pinned interfaces or prototypes.
They may not freeze the final W3 contract language, create production FAR API/MCP semantics,
or claim utility before the governed workstreams authorize those conclusions.

## Failure behavior

When a tool is unavailable, nondeterministic, rate-limited, or returns malformed output, the
failure is preserved. The status is not silently converted to absence, success, or proof. A
campaign may retry under its protocol, but every retry receives a distinct invocation identity
and the adjudication cites the exact selected invocations.
