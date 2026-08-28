# Finite exact-contract playground

Status: **Experimental and noncanonical**

[`exact_contract_playground.py`](../../tools/exact_contract_playground.py) accepts a finite
case set, finite test set, complete behavior table, and proposed representation. It reports:

- exact sufficiency or insufficiency;
- an image-level decoder when constructible;
- the first deterministic collision witness and all finite collisions;
- observational equivalence classes and quotient map;
- whether a sufficient representation is equivalent to or strictly more informative than the
  observational quotient.

Examples are under [`examples/exact-contract-playground/`](../../examples/exact-contract-playground/).
The command exits `0` for sufficient, `1` for an explicit collision, and `2` for malformed
input. Output ordering and identifiers are deterministic.

This is not the production FAR engine, not an API/MCP contract, and not the future W3 contract
language. It implements only finite exact tables and cannot prove an open-domain or
computability result. Its purpose is to expose the executable surface of FAR-CORE-001/002 and
provide negative controls for FAR-CORE-012.
