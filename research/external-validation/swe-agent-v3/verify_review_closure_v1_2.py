"""Required review-closure verifier for frozen v1.2 plus additive prospective hardening."""
from __future__ import annotations

import argparse
from pathlib import Path

import verify_review_closure_required_impl as _impl

for _name, _value in vars(_impl).items():
    if not _name.startswith("__"):
        globals()[_name] = _value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate static FAR-SWE-V3-001 review closure or an instantiated preexecution task/evidence pair."
    )
    parser.add_argument("--task-manifest", type=Path)
    parser.add_argument("--evidence-registry", type=Path)
    args = parser.parse_args(argv)
    if (args.task_manifest is None) != (args.evidence_registry is None):
        parser.error("--task-manifest and --evidence-registry must be supplied together")

    try:
        if args.task_manifest is not None:
            validate_instantiated_task_manifest(args.task_manifest, args.evidence_registry)
            print(
                "PASS: instantiated task population, task identities, retained evidence bytes, strata, "
                "repository caps, and frozen v1.2/additive hardening verify; this validation does not authorize execution."
            )
            return 0

        validate()
        if launch_authorization_open():
            raise DesignError(
                "pilot/confirmatory authorization cannot be validated without --task-manifest and --evidence-registry"
            )
    except DesignError as exc:
        print(f"FAIL: {exc}")
        return 1

    print(
        "PASS: static frozen v1.2 and additive classification-input hardening verify; "
        "no instantiated launch population was validated and execution remains blocked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
