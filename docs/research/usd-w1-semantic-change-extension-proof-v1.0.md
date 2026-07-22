# USD-W1-SC-001 v1.0 — Semantic-Change Scope Extension

## Status

Complete bounded extension proof for `S_sem_eff`.

## Frozen question

Can the theorem-facing target class uniformly represent effectively presented semantic change while preserving versioned denotation, inferential role, translation effects, unresolved correspondences, and historical dependencies, without equating label identity with semantic identity or importing semantic oracles?

## Source class

`S_sem_eff` contains countably named systems with a computable sequence of finite semantic-interface versions. Every change event explicitly records whether commitments are preserved, split, merged, introduced, retired, or unresolved. Each finite query has a finite effectively recoverable semantic dependency cone.

Undeclared reinterpretation, noncomputable transitions, retroactive erasure, unbounded global rewrites without finite dependency accounts, oracle-defined identity, and actual-process correspondence are excluded.

## Construction

For every admitted source, construct one target object containing distinct interpretation versions, explicit semantic-transition objects, version-indexed commitments and rules, declared partial-correspondence maps, reasons and rejected alternatives, and one uniform finite-query recovery interface.

The construction does not infer equivalence from shared spelling. A stable label may change denotation or inferential role; a changed label may preserve both. Translation outcomes remain typed as preserved, split, merged, introduced, retired, or unresolved.

## Preservation argument

For each finite semantic query, the source version, denotation, inferential role, transition classification, commitments, grounds, and dependency cone are recoverable from the target. Earlier semantic states are append-only and remain available when later changes alter admissibility or conclusions. Unresolved translations are never silently promoted to equivalence.

## Obligation results

All nine `SC-EXT` obligations pass for `S_sem_eff`: uniform construction; denotation; inferential role; translation effects; commitment-ground-dependency distinctions; semantic history; explicit unresolved translation; rejection of label collapse; and negative-control rejection.

## Adversarial controls

`SC-NEG-LABEL-001` is rejected because unchanged spelling does not preserve changed denotation or inference. `SC-NEG-ERASE-001` is rejected because overwriting prior semantics destroys the historical explanation of earlier commitments. Oracle-defined equivalence and unbounded retroactive semantic rewrites remain scope boundaries.

## Terminal classification

`proper_subclass_only`.

This proves faithful representation for `S_sem_eff`; it does not establish all semantic change, global decidability of semantic equivalence, general `S_IRD` representation, or universal structure.

## Claim effect

This is a fifth bounded feature-family result for `THM-IRD-EXT-001`. It establishes no necessity, minimality, uniqueness, actual-process correspondence, mechanized verification, or independent review.
