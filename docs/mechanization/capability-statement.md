# Mechanization Capability Statement

The current mechanization loads FAR YAML/IR artifacts, validates schema-level and reference-level well-formedness, constructs dependency graphs, detects representation-dependency cycles, inspects proof traces, and reports transition summaries.

The retained term `reasoning_engine.py` names a prototype trace-inspection and diagnostics tool. It does not perform general semantic inference, does not execute arbitrary reasoning calculi, and does not provide machine-verified formal proofs.

Machine-readable capability levels are recorded in [`capabilities.yaml`](capabilities.yaml).


## Contract-relative boundary

The current `far-ir/1.0` implementation does not encode a complete comparison contract, behavior map, decoder/factorization certificate, collision witness, observational quotient, interpretation profile, interface frame, or approximation/cost order. It therefore cannot certify `FAR-CORE-001` or `FAR-CORE-002` merely by accepting a document.

Successor requirements are specified in [Contract-Relative FAR IR v1.1 Requirements](contract-relative-far-ir-v1.1-requirements.md). The proposed format identifier is `far-ir/1.1`. That specification is Provisional and is not an implemented format.

## Specification export boundary

The deterministic `far-spec-v1` export is version `1.1.0` and includes the byte-identical canonical core theory plus the synchronized definitions. Its schema identifier remains `far-ir/1.0`; exporting the theorem makes the authority available to consumers but does not implement `far-ir/1.1` or prove conformance to the theorem.
