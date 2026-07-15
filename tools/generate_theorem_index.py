#!/usr/bin/env python3
"""Generate or check Project FAR metadata indexes."""
from __future__ import annotations
import argparse, difflib, sys
from verify_theory import (
    GENERATED_AXIOM_INDEX, GENERATED_DEFINITION_INDEX, GENERATED_LEMMA_INDEX,
    GENERATED_PROPOSITION_INDEX, GENERATED_THEOREM_INDEX,
    build_index, load_axioms, load_definitions, load_lemmas, load_propositions,
    load_theorems, run_verification,
)


def expected_indexes():
    theorems=load_theorems(); propositions=load_propositions(); lemmas=load_lemmas(); definitions=load_definitions(); axioms=load_axioms()
    return {
        GENERATED_THEOREM_INDEX: build_index(theorems, "Theorem", "proof"),
        GENERATED_PROPOSITION_INDEX: build_index(propositions, "Proposition", "source"),
        GENERATED_LEMMA_INDEX: build_index(lemmas, "Lemma", "source"),
        GENERATED_DEFINITION_INDEX: build_index(definitions, "Definition", "source"),
        GENERATED_AXIOM_INDEX: build_index(axioms, "Axiom", "source"),
    }


def check_indexes() -> int:
    run_verification(False)
    stale=[]
    for path, expected in expected_indexes().items():
        actual = path.read_text(encoding='utf-8') if path.exists() else ''
        if actual != expected:
            diff=''.join(difflib.unified_diff(actual.splitlines(True), expected.splitlines(True), fromfile=str(path), tofile=f'{path} expected', n=3))
            stale.append((path,diff))
    if stale:
        print('Generated metadata index check failed: stale files detected', file=sys.stderr)
        for path,diff in stale:
            print(f'--- {path}', file=sys.stderr); print(diff[:4000], file=sys.stderr)
        return 1
    print('Generated metadata indexes are current')
    return 0


def write_indexes() -> int:
    run_verification(True)
    print('Wrote generated metadata indexes')
    return 0


def main() -> int:
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='compare generated indexes without writing')
    mode.add_argument('--write', action='store_true', help='write generated indexes')
    args=parser.parse_args()
    if args.write: return write_indexes()
    return check_indexes()
if __name__=='__main__': raise SystemExit(main())
