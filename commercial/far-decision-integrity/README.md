# FAR Decision Integrity Core

This package validates explicit `far-decision-package/0.1` artifacts and deterministically classifies them as:

- `justified`;
- `unsupported`;
- `underdetermined`;
- `unverifiable`.

It is the minimum reusable commercial core ported onto current `main` after the repository convergence audit.

## Use

```bash
python -m pip install ./commercial/far-decision-integrity
far-decision package.json --output report.json
```

## Claim boundary

This package evaluates disclosed package structure, dependencies, contradictions, alternatives, unknowns, and declared trace completeness. It does not infer hidden reasoning, prove external factual truth, establish trace completeness, certify safety, or certify legal compliance.

## Next dependency

The next tranche may compile ordinary external agent traces into this package contract while preserving observed, derived, inferred, declared, contradicted, missing, and unverifiable evidence distinctions.
