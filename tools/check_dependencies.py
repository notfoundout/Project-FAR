#!/usr/bin/env python3
"""Run Project FAR dependency and circularity checks."""

from verify_theory import load_theorems, validate_dependencies, validate_no_cycles, VerificationError

if __name__ == "__main__":
    try:
        graph = validate_dependencies(load_theorems())
        validate_no_cycles(graph)
    except VerificationError as exc:
        print(f"DEPENDENCY CHECK FAILED: {exc}")
        raise SystemExit(1)
    print("DEPENDENCY CHECK PASSED")
