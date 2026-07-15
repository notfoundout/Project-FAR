# Mechanization Capability Statement

The current mechanization loads FAR YAML/IR artifacts, validates schema-level and reference-level well-formedness, constructs dependency graphs, detects representation-dependency cycles, inspects proof traces, and reports transition summaries.

The retained term `reasoning_engine.py` names a prototype trace-inspection and diagnostics tool. It does not perform general semantic inference, does not execute arbitrary reasoning calculi, and does not provide machine-verified formal proofs.

Machine-readable capability levels are recorded in [`capabilities.yaml`](capabilities.yaml).
