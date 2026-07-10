# Purpose

This document records the executable Phase 3 testing boundary for the mechanization MVP.

# Test Layers

Tests cover canonical IR records, external models and schema conversion, JSON/YAML parsing, normalization, deterministic serialization, graph construction and dependency validation, CLI behavior, conformance cases, end-to-end pipelines, packaging smoke checks, security safeguards, and MVP-scale performance safeguards.

# Commands

Required local validation commands are:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python tools/validate_docs.py
python tools/check_internal_links.py
python tools/check_dependencies.py
python tools/check_markdown_hygiene.py
python tools/verify_theory.py
git diff --check
python -m pytest
python -m pytest tests/mechanization -q
python -m mechanization.far_mechanization.conformance
python -m mechanization.far_mechanization.conformance --output json
far version
far help
```

# Performance Safeguards

The test suite generates a 1,000-node acyclic graph and a 1,000-node dependency chain. Assertions check completion, stable counts, non-recursive traversal behavior, multiple-cycle reporting, normalization idempotence, and deterministic repeated serialization rather than fragile wall-clock thresholds.

# Regression Policy

Prompt 1–5 tests remain active. Prompt 6 adds conformance and end-to-end coverage without weakening earlier assertions.
