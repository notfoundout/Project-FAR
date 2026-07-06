#!/usr/bin/env python3
"""Run Project FAR derived-concept registry checks."""

from verify_theory import load_theorems, validate_registry, VerificationError

if __name__ == "__main__":
    try:
        validate_registry(load_theorems())
    except VerificationError as exc:
        print(f"REGISTRY CHECK FAILED: {exc}")
        raise SystemExit(1)
    print("REGISTRY CHECK PASSED")
