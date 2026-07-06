# Universal Structure Falsification Framework

Status: Provisional

## Failure condition

FAR's current primitive architecture fails if an explicit reasoning system cannot be represented with the accepted primitives and cannot be handled by accepted conservative mechanisms.

A counterexample succeeds when the reasoning system:

1. is explicit reasoning;
2. cannot be represented with Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus;
3. cannot be reduced to registered derived concepts;
4. cannot be handled by adding a conservative extension;
5. requires a genuinely new primitive.

## Evidence required

A falsification claim must provide a machine-readable fixture and a prose analysis showing the failed primitive mapping, the attempted reductions, the failed conservative-extension path, and the proposed new primitive.

## Outcomes

- `fits FAR`: all required primitive mappings are supplied without unresolved gaps.
- `extends FAR`: the system requires conservative derived concepts but no new primitive.
- `falsifies FAR`: the system satisfies the counterexample criteria above.
- `draft`: the fixture is incomplete and cannot yet decide the outcome.
