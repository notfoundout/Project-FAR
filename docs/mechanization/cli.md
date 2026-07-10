# Purpose

The FAR CLI exposes the implemented Phase 3 mechanization capabilities for validation, parsing, normalization, graph construction, diagnostics, statistics, export, inspection, version reporting, and help.

# Installation

Install declared dependencies with `python -m pip install -r requirements.txt`. The repository entrypoint is `./far`, and the module entrypoint is `python -m mechanization.far_mechanization.cli`.

# Commands

Implemented commands are `far validate`, `far parse`, `far normalize`, `far graph`, `far diagnostics`, `far stats`, `far export`, `far inspect`, `far version`, and `far help`.

# Options

Global options include `--config`, `--output text|json|yaml`, `--quiet`, `--verbose`, and `--color auto|always|never`. File commands support `--format json|yaml`; `far normalize` supports `--write` and `--force`; `far graph` supports `--export`; `far diagnostics` supports `--sort severity|code|source`; `far export` supports `--kind json|yaml|graph-json` and `--output-file`.

# Exit Codes

Commands return `0` on success and non-zero on invalid input, failed validation, missing files, unsafe overwrite attempts, or write errors.

# Configuration

Configuration is optional YAML loaded with `--config`. Supported keys are `output`, `quiet`, `verbose`, and `color`. Precedence is CLI arguments, configuration file, then defaults.

# Diagnostics

The CLI reuses the existing structured diagnostic model. Diagnostics include stable codes, severity, messages, source locations when available, related identifiers, and details.

# Reports

The CLI produces validation summaries, graph summaries, dependency diagnostics, diagnostic summaries, and statistics summaries in human-readable or JSON output where supported.

# Examples

Executable examples are provided under `examples/mechanization/cli/` for validate, parse, normalize, graph, diagnostics, export, stats, and inspect.

# Machine-readable Output

Use `--output json` for machine-readable command output. `far export --kind graph-json` emits a JSON graph export with nodes, edges, and statistics.

# Deferred Features

Proof verification, automated reasoning, REST API, persistent storage, and arbitrary operation execution remain deferred.
