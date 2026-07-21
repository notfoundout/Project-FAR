# FAR-VAL-GEN-002 — Generated artifact drift

The generator completed but changed one or more files in its isolated repository copy.

1. Reproduce the focused check with `python -m far_validation validate <check-id> --no-cache`.
2. Inspect the `changed_files` field and failure bundle.
3. Determine whether the generator or committed artifact is authoritative.
4. Correct the stale side; do not blindly overwrite an artifact when the generator itself may be wrong.
5. Run the focused check, affected closure, and full profile before merge.
