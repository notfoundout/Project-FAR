# Repository Health Checks

Status: Provisional maintenance tooling

## Purpose

The repository health check is a single maintenance entry point for validating Project FAR before merge. It collects existing theory, registry, notation, circularity, evaluation, documentation, YAML, Markdown, link, release, FAR example, and proof-object checks without changing theory meaning.

## When to run `--fast`

Run the fast health check after ordinary changes and before opening or updating a pull request:

```bash
python tools/repo_health_check.py --fast
```

`--fast` is intended for CI and skips slower evaluation runs while still checking repository hygiene, documentation hygiene, internal links, math displays, release consistency, FAR example smoke tests, and proof-object smoke tests.

## When to run `--full`

Run the full health check before releases or broad maintenance changes:

```bash
python tools/repo_health_check.py --full
```

`--full` includes the fast checks plus slower evaluation and adversarial-suite checks when the corresponding tools are present.

## Checker summary

- `tools/repo_health_check.py` runs the repository-wide health suite and reports pass, warning, and failure status.
- `tools/validate_docs.py` runs the docs-only validation suite.
- `tools/check_internal_links.py` finds broken relative Markdown, image, and file links in Markdown and YAML files.
- `tools/check_math_rendering.py` detects unclosed display math, malformed fenced math, and broken math-display image links.
- `tools/check_release_consistency.py` checks that README release references point to the newest release documentation and tag.
- `tools/check_orphaned_docs.py` reports Markdown files that are not reachable from major navigation roots.
- `tools/check_repository_hygiene.py` validates YAML parsing, duplicate machine-readable IDs, and registry-like file references.
- `tools/check_markdown_hygiene.py` checks malformed tables, empty links, duplicate heading anchors, missing image alt text, and unclosed code fences.

## Warnings vs failures

Failures are clear problems that should block merge, such as invalid YAML, missing required links, stale current-release references, unclosed code fences, or failed proof-object checks.

Warnings identify issues that may be intentional or require human judgment, such as orphaned standalone documentation, duplicate heading anchors, image links without alt text, or uncertain inline math delimiter use.

## Fixing common failures

### Broken internal links

Run `python tools/check_internal_links.py`, then update the source link or restore the missing target path printed by the checker.

### Broken math display

Run `python tools/check_math_rendering.py`. Add missing closing `$$`, `\]`, or code fences, or repair missing math-display image files.

### Stale release links

Run `python tools/check_release_consistency.py`. Update README latest-release prose, release-document links, and release badge or tag links to match the newest `docs/releases/project-far-v*.md` file.

### Invalid YAML

Run `python tools/check_repository_hygiene.py`. Fix the syntax error reported with the file path and parser message.

### Duplicate IDs

Keep IDs unique within machine-readable registries, adversarial suites, and proof objects. Rename only tooling or registry identifiers when the change does not alter theory meaning.

### Orphaned docs

Run `python tools/check_orphaned_docs.py`. Add a navigation link from a relevant index, move intentional standalone notes under `archive/`, or mark the file with `orphan-ok` only when standalone status is intentional.

### Malformed Markdown tables

Run `python tools/check_markdown_hygiene.py`. Make each row in a table block use the same number of columns.

### Failed FAR parsing

Run the command printed by `tools/repo_health_check.py` for the failing `examples/far/**/*.far.yaml` file and fix YAML or example structure without changing parser behavior.

### Failed proof-object checks

Run the printed `tools/check_proof_object.py` command for the failing proof object and repair validation metadata only when allowed by the project governance and PR scope.

## Recommended workflow before merge

```bash
make health-fast
```

Before release:

```bash
make health
```
