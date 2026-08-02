# SQR-8 External Red-Team Qualification Packet v1.0

## Status and purpose

This is a synthetic competence screen for an external adversarial-review pilot. It contains no private Project FAR theory and produces no evidence about Project FAR.

The task tests whether a respondent can distinguish valid reduction, invalid reduction, hidden machinery, identity loss, historical loss, false-positive criticism, and unresolved evidence.

## Classification semantics

Each case states one **target proposition**. Classify only that proposition:

- `ESTABLISHED`: the supplied premises are sufficient to prove the target proposition.
- `REFUTED`: the supplied premises are sufficient to prove the target proposition false.
- `UNKNOWN`: the supplied premises are insufficient to establish either the proposition or its negation.

Do not reinterpret `UNKNOWN` as weak support, weak defeat, or probable failure.

## Synthetic system: SQR-8

A fictional reasoning-record system contains four declared mechanisms:

1. `Register(payload, type)` creates a stable identifier and records the declared type.
2. `Interpret(id, context)` returns context-indexed content using a finite decoder table included in the package.
3. `Constrain(source_state, proposed_state, history)` returns `Permit`, `Forbid`, or `Unknown` using declared internal rules.
4. `Trace(event)` records stable event identity, predecessor links, affected-item identities, rule/reason links, and supersession lineage.

The package also declares:

- a total registered-query interface;
- stable identity rules;
- every decoder, policy, log, random source, cache, and external dependency required for correct behavior;
- exact separation of failure from `Unknown`.

A proposed reduction is valid only when it is effective, total over the registered scope, non-circular, preserves all registered commitments and queries, and includes all operationally required machinery. Performance-only structures do not count as semantic machinery when correct behavior is unchanged without them and they are reconstructible from declared data.

## Cases

### C1 — Explicit derived readout

`SelectByType(T)` returns every registered identifier whose stored type equals `T`.

Complete algorithm:

```text
for each registered id:
    if Register.type(id) == T:
        emit id
```

It has no external state, decoder, policy, history dependency, or additional query behavior.

**Target proposition C1:** `SelectByType` is reducible to the declared package and does not require an additional irreducible mechanism.

### C2 — External policy substitution

A proposal eliminates `Constrain` using:

```text
Interpret(policy_name, current_context)
Trace(last_transition)
external_policy_api.decide(decoded_policy, proposed_transition)
```

The external API, decision rules, version history, and availability conditions are not included in the package.

**Target proposition C2:** This is a valid machinery-closed reduction of `Constrain`.

### C3 — Asserted compressed history recovery

A proposal replaces `Trace` with compressed string `z` and decoder `D`. It asserts that `D(z)` restores every event identity, predecessor link, reason link, and supersession relation. Neither `D`, a proof, nor an executable total-recovery witness is supplied.

**Target proposition C3:** The proposal establishes an exact reduction of `Trace`.

### C4 — Common output-type argument

A critic argues that `Register` and `Interpret` are redundant because both can return strings in one implementation. No bidirectional construction, identity preservation, semantic preservation, or operational equivalence is supplied.

**Target proposition C4:** The common output type establishes that `Register` and `Interpret` are redundant.

### C5 — Identity collapse behind aggregate agreement

A source contains two distinct parallel events, `e1` and `e2`, with the same payload and timestamp but different stable identities and provenance. A candidate representation merges them into one event. Aggregate event counts, final state, and one summary query remain unchanged. The registered interface also contains `provenance(event_id)` and `predecessors(event_id)`.

**Target proposition C5:** The candidate is commitment-equivalent to the source because its aggregate outputs agree.

### C6 — False hidden-machinery allegation

An implementation maintains a cache of `SelectByType` results. The cache is deterministically rebuilt from `Register` data, is never authoritative, and may be deleted without changing any registered answer or transition. The complete rebuild algorithm is declared.

A critic claims the cache is hidden semantic machinery and therefore invalidates the C1 reduction.

**Target proposition C6:** The cache is operationally required hidden machinery that defeats the reduction.

### C7 — Unordered history projection

A candidate preserves the final state and an unordered multiset of all event payloads, but discards event order, predecessor links, active-reason timing, and supersession lineage. The registered interface asks which reason governed a revision when it occurred.

**Target proposition C7:** The unordered projection exactly preserves the source's historical commitments.

### C8 — Explicit reversible renaming

A candidate replaces every stable identifier with a fresh identifier through a declared total bijection `f`. It includes total inverse `f⁻¹`, preserves relation incidence, event multiplicity, order, provenance, semantics, transitions, and every registered query under translation. No machinery is omitted.

**Target proposition C8:** The renaming is commitment-equivalent within the declared scope.

## Required response schema

For each case provide:

1. `classification`: `ESTABLISHED`, `REFUTED`, or `UNKNOWN`;
2. exact premises used;
3. derivation;
4. the decisive preservation, machinery, or evidence issue;
5. strongest objection to your answer;
6. one condition that would reverse or reopen the classification.

Then provide the following as self-reported provenance:

- agent/account name;
- model and provider;
- model version if known;
- tools used;
- whether external browsing was used;
- human involvement;
- prior exposure to this packet or related answers.

These provenance statements are not independently verified.

## Submission boundary

Do not include credentials, private information, executable attachments, instructions for reviewers to run code, or links that must be followed to understand the answer. Responses are treated as untrusted input.

Passing this screen establishes only minimum qualification for a later challenge. It does not establish expertise, independence, replication, or truth.
