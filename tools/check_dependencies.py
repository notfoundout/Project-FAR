#!/usr/bin/env python3
"""Run Project FAR dependency and circularity checks."""

from verify_theory import (
    VerificationError,
    load_lemmas,
    load_propositions,
    load_theorems,
    validate_dependencies,
    validate_no_cycles,
)

if __name__ == "__main__":
    try:
        graph = validate_dependencies(load_theorems(), load_propositions(), load_lemmas())
        validate_no_cycles(graph)
    except VerificationError as exc:
        print(f"DEPENDENCY CHECK FAILED: {exc}")
        raise SystemExit(1)
    print("DEPENDENCY CHECK PASSED")
