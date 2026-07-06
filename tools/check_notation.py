#!/usr/bin/env python3
"""Run Project FAR canonical notation checks."""

from verify_theory import validate_notation_file, VerificationError

if __name__ == "__main__":
    try:
        validate_notation_file()
    except VerificationError as exc:
        print(f"NOTATION CHECK FAILED: {exc}")
        raise SystemExit(1)
    print("NOTATION CHECK PASSED")
