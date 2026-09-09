# FAR Decision Integrity Core

This package validates explicit decision packages and deterministically classifies them as:

- `justified`;
- `unsupported`;
- `underdetermined`;
- `unverifiable`.

`far-decision-package/0.2` adds a semantic-integrity lane without reinterpreting historical `far-decision-package/0.1` packages. Version 0.1 remains readable, but only 0.2 may carry `semantic_contracts`.

## Semantic integrity

A 0.2 package may embed one or more governed FAR IR records in `semantic_contracts`. The commercial package does **not** reimplement FAR IR semantics. It locates the canonical Project FAR repository, invokes the governed `far-ir/2.0` or `far-ir/2.1` verifier, and records SHA-256 identities for the exact verifier and schema used.

The adjudication mapping is fail-closed:

- a valid `PROVED` FAR IR record clears only its semantic gate;
- a valid `REFUTED` record is `semantic-material-loss` and forces `unsupported`;
- a valid `Unknown` record is not evidence of preservation and yields `unverifiable` unless a stronger existing status applies;
- malformed or semantically invalid FAR IR evidence yields `unverifiable`;
- an unavailable or crashing canonical verifier yields `unverifiable`, never success.

A semantic `PROVED` result cannot override contradicted evidence, missing authorization, material alternatives, declared unknowns, or incomplete traces.

## Use

From a Project FAR checkout:

```bash
python -m pip install ./commercial/far-decision-integrity
far-decision package.json --require-semantic-contract --output report.json
```

If the package is installed outside the checkout, set `FAR_REPO_ROOT` to the canonical Project FAR repository root. `--require-semantic-contract` makes absence of a semantic contract fail closed as `unverifiable`; without the flag, legacy and non-semantic workflows preserve their existing behavior.

A 0.2 package extends the previous shape with:

```json
{
  "schema_version": "far-decision-package/0.2",
  "semantic_contracts": [
    {
      "format_version": "far-ir/2.0",
      "id": "example.semantic.audit",
      "contract": {},
      "report": {},
      "provenance": {},
      "freeze": {}
    }
  ]
}
```

The embedded FAR IR object must satisfy its own canonical schema and semantic verifier; the abbreviated object above only shows placement.

## Claim boundary

This package evaluates disclosed package structure, dependencies, contradictions, alternatives, unknowns, declared trace completeness, and the finite explicit semantics actually encoded in supplied FAR IR records. It does not infer hidden reasoning, prove external factual truth, establish that a domain mapping is correct or complete, certify safety, certify legal compliance, establish empirical utility, or establish novelty.

A `justified` decision means that no failure is present under the disclosed package rules and any required semantic contracts passed their recorded FAR verifier. It is not a universal truth or safety certificate.
