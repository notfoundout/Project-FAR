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
