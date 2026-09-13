"""Public FAR intake API and command-line entry point.

All input, schema, and semantic checks live in one implementation so every caller
uses the same validation boundary without import-time mutation or reload hooks.
"""
from ._intake_v1_core import (  # noqa: F401
    FORMAT_VERSION,
    SCHEMA_PATH,
    _json_native_errors,
    _strict_json_loads,
    _terminal_saturation_errors,
    aggregate_manifest,
    canonical_json,
    freeze_manifest,
    main,
    new_manifest,
    sha256_json,
    sha256_text,
    validate_manifest,
)


if __name__ == "__main__":
    raise SystemExit(main())
