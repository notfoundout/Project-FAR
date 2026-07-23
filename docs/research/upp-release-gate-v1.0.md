# Universal Proof Release Gate

Public evaluation remains unauthorized during UPP-W0 through UPP-W14.

The terminal UPP-W15 adjudication may authorize public evaluation only if it records, in one auditable package:

- the exact quantified theorem;
- the independently defined domain, class, contract, and representation family;
- the machinery-closure and equivalence rules;
- every assumption and its classification;
- the machine-checked status of every central lemma;
- any admitted axiom, unresolved obligation, or weakened conclusion;
- the selected terminal outcome;
- all surviving nonclaims.

A passing repository health check, artifact validator, test suite, or proof-assistant build does not authorize release unless the central theorem itself is represented in the proof dependency graph and the terminal audit confirms that no required claim survives only in prose or generated data.
