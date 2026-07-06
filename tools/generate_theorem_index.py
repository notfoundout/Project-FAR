#!/usr/bin/env python3
"""Generate the Project FAR theorem index from YAML metadata."""

from verify_theory import main

if __name__ == "__main__":
    raise SystemExit(main(["--write-index"]))
