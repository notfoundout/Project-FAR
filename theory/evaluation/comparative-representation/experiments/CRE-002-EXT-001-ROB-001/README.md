# CRE-002-EXT-001-ROB-001

## Status

Automated multi-implementation robustness track replacing the unexecuted human-team track `CRE-002-EXT-001-REP-001`.

## Purpose

Test whether the frozen CRE-002-EXT-001 scenario survives multiple separately written computational implementations rather than depending on one implementation body.

## Architecture

The executable package contains three distinct compiler source files:

- `tools/cre002_compilers/compiler_recursive.py`
- `tools/cre002_compilers/compiler_iterative.py`
- `tools/cre002_compilers/compiler_pairs.py`

It also contains a separately implemented verifier:

- `tools/cre002_compilers/verifier.py`

Each compiler runs as its own process in a private temporary working directory. It receives only a private copy of the frozen input and its output path. Compiler outputs are not copied into the verifier workspace until all compiler processes finish. The verifier compares each output to the frozen scenario, requires byte-identical canonical serialization, and runs registered mutation and malformed-input tests. A complete second execution must reproduce the same report and digest.

The implementations are separate source files and use materially different traversal strategies: recursive reconstruction, iterative stack reconstruction, and object-pair materialization. They remain controlled by one repository and one development process.

## Claim boundary

A passing result establishes **bounded multi-implementation robustness**. It shows that the frozen scenario survives three separately written computational paths, process/workspace isolation, a separate verifier, registered mutations, malformed inputs, and deterministic rerun.

It is not independent external replication. It does not establish independent human judgment, independent organizational incentives, independent specification interpretation, or absence of shared specification-level mistakes.

## Execution

```bash
python tools/cre002_ext001_robustness.py --check
python -m unittest tests.test_cre002_ext001_rep001_team_registry
```

## Supported conclusion

Only this conclusion is licensed by a passing run:

> For the frozen CRE-002-EXT-001 scenario, three distinct compiler source implementations running in isolated workspaces produced the same canonical result; a separate verifier accepted the unmodified outputs, rejected the registered mutations and malformed cases, and a full rerun reproduced the same report and digest.

No external-replication, universal-sufficiency, necessity, minimality, human-independence, organizational-independence, superiority, FAR-proof, or universal-structure conclusion follows.
