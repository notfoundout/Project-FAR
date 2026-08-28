#!/usr/bin/env python3
"""Independent finite checks for the exact PR #453 SSS-3 witnesses.

This is deliberately not a repository test.  It reconstructs cut-free,
unit-free one-sided MLL proof search for the tiny witness fragment and checks
the complete four-member uniform monotone successor-set decoder class.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
import json


Formula = tuple
Sequent = tuple[Formula, ...]


def atom(name: str, positive: bool = True) -> Formula:
    return ("atom", name, positive)


def tensor(left: Formula, right: Formula) -> Formula:
    return ("tensor", left, right)


def par(left: Formula, right: Formula) -> Formula:
    return ("par", left, right)


def key_formula(formula: Formula) -> str:
    return repr(formula)


def canonical(sequent: Sequent) -> Sequent:
    return tuple(sorted(sequent, key=key_formula))


def dual_atoms(left: Formula, right: Formula) -> bool:
    return (
        left[0] == right[0] == "atom"
        and left[1] == right[1]
        and left[2] != right[2]
    )


@lru_cache(maxsize=None)
def provable(sequent: Sequent) -> bool:
    """Cut-free provability for the unit-free MLL fragment used here."""
    sequent = canonical(sequent)
    if len(sequent) == 2 and dual_atoms(sequent[0], sequent[1]):
        return True

    # One-sided par rule: Gamma,A,B / Gamma,A par B.
    for index, formula in enumerate(sequent):
        if formula[0] == "par":
            rest = sequent[:index] + sequent[index + 1 :]
            if provable(canonical(rest + (formula[1], formula[2]))):
                return True

    # One-sided tensor rule: split the remaining multiset between premises.
    for index, formula in enumerate(sequent):
        if formula[0] != "tensor":
            continue
        rest = sequent[:index] + sequent[index + 1 :]
        for mask in range(1 << len(rest)):
            gamma = tuple(rest[i] for i in range(len(rest)) if mask & (1 << i))
            delta = tuple(rest[i] for i in range(len(rest)) if not mask & (1 << i))
            if provable(canonical(gamma + (formula[1],))) and provable(
                canonical(delta + (formula[2],))
            ):
                return True
    return False


def projected_successors(sequent: Sequent) -> set[Sequent]:
    """All individual premises after forgetting their rule-instance grouping."""
    successors: set[Sequent] = set()
    for index, formula in enumerate(sequent):
        if formula[0] == "par":
            rest = sequent[:index] + sequent[index + 1 :]
            successors.add(canonical(rest + (formula[1], formula[2])))
        elif formula[0] == "tensor":
            rest = sequent[:index] + sequent[index + 1 :]
            for mask in range(1 << len(rest)):
                gamma = tuple(rest[i] for i in range(len(rest)) if mask & (1 << i))
                delta = tuple(rest[i] for i in range(len(rest)) if not mask & (1 << i))
                successors.add(canonical(gamma + (formula[1],)))
                successors.add(canonical(delta + (formula[2],)))
    return successors


def truth_set(sequent: Sequent) -> frozenset[int]:
    return frozenset(int(provable(s)) for s in projected_successors(sequent))


def decoder_table() -> dict[str, tuple[int, int, int]]:
    """All monotone triples on {0}->{0,1}->{1}; exactly four."""
    triples = [bits for bits in product((0, 1), repeat=3) if bits[0] <= bits[1] <= bits[2]]
    names = {
        (0, 0, 0): "TERM",
        (0, 0, 1): "AND",
        (0, 1, 1): "OR",
        (1, 1, 1): "NONEMPTY",
    }
    assert len(triples) == 4
    assert set(triples) == set(names)
    return {names[triple]: triple for triple in triples}


def decode(name: str, values: frozenset[int]) -> int:
    if not values:
        return 0
    triple = decoder_table()[name]
    index = {frozenset({0}): 0, frozenset({0, 1}): 1, frozenset({1}): 2}[values]
    return triple[index]


def main() -> None:
    a = atom("a")
    a_perp = atom("a", False)
    b = atom("b")
    b_perp = atom("b", False)

    s_or = canonical((a_perp, a_perp, tensor(a, b)))
    s_and = canonical((a_perp, b_perp, tensor(a, b)))

    assert not provable(s_or)
    assert provable(s_and)
    assert truth_set(s_or) == frozenset({0, 1})
    assert truth_set(s_and) == frozenset({0, 1})

    failures: dict[str, str] = {}
    for name in decoder_table():
        predicted_or = decode(name, truth_set(s_or))
        predicted_and = decode(name, truth_set(s_and))
        if predicted_or != int(provable(s_or)):
            failures[name] = "S_or"
        elif predicted_and != int(provable(s_and)):
            failures[name] = "S_and"
        else:
            raise AssertionError(f"decoder {name} unexpectedly succeeds on both witnesses")

    assert failures == {
        "TERM": "S_and",
        "AND": "S_and",
        "OR": "S_or",
        "NONEMPTY": "S_or",
    }

    result = {
        "check": "independent_pr453_sss3_finite_witness_reconstruction",
        "decoder_count": len(decoder_table()),
        "decoders": {name: list(bits) for name, bits in decoder_table().items()},
        "witnesses": {
            "S_or": {
                "provable": provable(s_or),
                "projected_successor_count": len(projected_successors(s_or)),
                "successor_truth_set": sorted(truth_set(s_or)),
            },
            "S_and": {
                "provable": provable(s_and),
                "projected_successor_count": len(projected_successors(s_and)),
                "successor_truth_set": sorted(truth_set(s_and)),
            },
        },
        "refuting_witness_by_decoder": failures,
        "result": "PASS",
        "interpretation": "finite consistency plus exhaustive check of the stated four-decoder class; not a substitute for the general proofs"
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
