# UPP-W9 Dependency-Structure Necessity

## Theorem

Relative to the frozen target class `C*`, faithfulness contract `P*`, admissible representation universe `E*`, machinery closure, and commitment-equivalence relation, a fully faithful representation that answers registered dependency queries must expose a recoverable typed dependency structure.

The theorem is operational and conditional. It does not claim that every conceivable relation is an objective dependency, nor that dependency is metaphysically primitive.

## Witness

The witness is a nonempty directed relation over represented identities. Every edge has:

- a stable edge identity;
- resolved source and target identities;
- one of the frozen kinds: support, defeat, revision, replacement, admissibility, or provenance;
- an explicit temporal scope;
- an effective recovery procedure;
- operational relevance to permitted inference, revision, replacement, admissibility, or explanation;
- invariance under the frozen representation equivalence;
- complete machinery accounting.

A positive theorem result additionally requires at least one support or defeat edge. A graph consisting only of provenance annotations is not enough to establish reasoning dependency.

## Proof strategy

1. Full dependency preservation requires answers to registered questions about what supports, defeats, revises, replaces, admits, or produced a represented item.
2. Totality requires each answer to be recoverable, explicitly failed, or Unknown.
3. Machinery closure charges all graph stores, indexes, decoders, reason extractors, and oracle realizations to the representation.
4. Commitment equivalence prevents syntax or medium changes from altering edge identity, direction, kind, or temporal scope.
5. Therefore, when all antecedents pass, the recovered nodes and edges construct the required dependency witness.
6. Denial of the witness contradicts dependency preservation, query totality, machinery closure, or equivalence stability.

## Separating countermodels

The theorem rejects systems with identical conclusions but different support graphs, removed defeating edges, temporal succession without dependence, correlation without recoverable direction, hidden provenance services, representation-dependent edge types, and absent edges manufactured by collapsing Unknown into failure.

## Claim boundary

This closes the flat-state and temporal-correlation loopholes for R3. It leaves semantic interpretation, historical identity, sufficiency, irreducibility, maximality, and the terminal theorem unresolved.
