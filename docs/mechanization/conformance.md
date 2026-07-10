# Purpose

The Phase 3 conformance suite records executable `far-ir/1.0` behavior for document shape, parsing, references, graph construction, dependencies, normalization, serialization, and CLI behavior.

# Suite Layout

The suite lives under `conformance/far-ir-1.0/` with a README, `manifest.json`, valid inputs, invalid inputs, and golden expected outputs. The manifest is the canonical index for stable case identifiers, categories, expected validity, expected diagnostic codes, optional golden normalization output, optional graph statistics, and notes.

# Runner

Run the suite with:

```bash
python -m mechanization.far_mechanization.conformance
python -m mechanization.far_mechanization.conformance --output json
far conformance --output json
```

The runner exits zero only when every manifest case passes. It does not rewrite golden files during ordinary execution.

# Golden Outputs

Golden files in `conformance/far-ir-1.0/expected/` are deterministic review artifacts for normalized JSON, normalized YAML, graph JSON, and diagnostics JSON. Regeneration is a manual developer operation; no automatic golden update command is provided in Phase 3.

# Coverage

The suite includes 58 cases across document structure, parsing, references, graph construction, dependencies, normalization, serialization, and CLI behavior.
