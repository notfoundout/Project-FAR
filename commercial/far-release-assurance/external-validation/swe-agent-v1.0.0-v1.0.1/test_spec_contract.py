from __future__ import annotations

REQUIRED_TEST_SPEC_PROPERTIES = frozenset(
    {
        "base_dockerfile",
        "env_dockerfile",
        "instance_dockerfile",
        "setup_env_script",
        "install_repo_script",
        "eval_script",
        "base_image_key",
        "env_image_key",
        "instance_image_key",
        "platform",
    }
)


def verify_test_spec_contract(spec: object) -> None:
    missing = sorted(name for name in REQUIRED_TEST_SPEC_PROPERTIES if not hasattr(spec, name))
    if missing:
        raise SystemExit(f"Pinned SWE-bench TestSpec contract mismatch; missing: {missing}")

    for name in REQUIRED_TEST_SPEC_PROPERTIES:
        value = getattr(spec, name)
        if value is None:
            raise SystemExit(f"Pinned SWE-bench TestSpec property is empty: {name}")
        if isinstance(value, str) and not value.strip():
            raise SystemExit(f"Pinned SWE-bench TestSpec property is empty: {name}")


def _result_spec(item: object) -> object:
    """Extract the TestSpec from the exact pinned build-result shapes.

    The pinned harness has returned both direct TestSpec objects and tuples with
    the TestSpec as element zero across adjacent helper paths. Accept only those
    explicit forms and fail closed on anything else.
    """
    if hasattr(item, "instance_id"):
        return item
    if isinstance(item, tuple) and item and hasattr(item[0], "instance_id"):
        return item[0]
    raise SystemExit(
        "Pinned SWE-bench build result contract mismatch; expected a TestSpec "
        "or a tuple whose first element is a TestSpec"
    )


def successful_instance_ids(successful: object) -> set[str]:
    try:
        items = list(successful)  # type: ignore[arg-type]
    except TypeError as exc:
        raise SystemExit("Pinned SWE-bench build result is not iterable") from exc

    instance_ids: set[str] = set()
    for item in items:
        spec = _result_spec(item)
        instance_id = getattr(spec, "instance_id", None)
        if not isinstance(instance_id, str) or not instance_id.strip():
            raise SystemExit(
                "Pinned SWE-bench build result contract mismatch; "
                "TestSpec instance_id is missing or empty"
            )
        instance_ids.add(instance_id)
    return instance_ids


def verify_build_result(successful: object, failed: object, expected_instance_id: str) -> None:
    if failed:
        raise SystemExit(f"Local SWE-bench image build reported failures: {failed!r}")
    built_ids = successful_instance_ids(successful)
    if expected_instance_id not in built_ids:
        raise SystemExit(
            "Local SWE-bench image build did not report the expected instance: "
            f"expected={expected_instance_id!r}, successful_instance_ids={sorted(built_ids)!r}"
        )
