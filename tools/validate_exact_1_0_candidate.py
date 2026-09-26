from __future__ import annotations

import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "commercial" / "far-decision-integrity" / "pyproject.toml"
READINESS = ROOT / "docs" / "releases" / "1.0-readiness.json"
REGISTRY = ROOT / "docs" / "releases" / "1.0-interface-registry.json"
NOTES = ROOT / "docs" / "releases" / "1.0.0-draft.md"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def validate_readiness(readiness: dict[str, object]) -> None:
    if readiness["previous_public_version"] != "0.4.0":
        raise SystemExit("release baseline must be 0.4.0")
    if readiness["target_version"] != "1.0.0":
        raise SystemExit("release target must be 1.0.0")

    expected_pending = {
        "exact_release_commit_validation",
        "explicit_publication_authorization",
    }
    status = readiness.get("status")
    completed = readiness.get("completed", {})
    if not isinstance(completed, dict):
        raise SystemExit("release completed-gates record must be an object")

    if status == "publication-authorized":
        if readiness.get("release_allowed") is not True:
            raise SystemExit("publication-authorized readiness must allow release")
        if readiness.get("remaining") != {}:
            raise SystemExit("publication-authorized readiness must have no remaining gates")
        for gate in expected_pending:
            if completed.get(gate) is not True:
                raise SystemExit(f"publication-authorized readiness lacks completed gate: {gate}")
    else:
        if readiness.get("release_allowed") is not False:
            raise SystemExit("validation PR must not authorize publication")
        remaining = readiness.get("remaining")
        if not isinstance(remaining, (dict, list, tuple, set)) or set(remaining) != expected_pending:
            raise SystemExit("unexpected remaining release gates")


def main() -> int:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    if project["version"] != "1.0.0":
        raise SystemExit("canonical package version must be 1.0.0")

    scripts = set(project["scripts"])
    expected = {"far-decision", "far-reasoning-regression", "far-external-trace"}
    if scripts != expected:
        raise SystemExit(f"public CLI mismatch: {sorted(scripts)}")

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    validate_readiness(readiness)

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_text = json.dumps(registry, sort_keys=True)
    for command in expected:
        if command not in registry_text:
            raise SystemExit(f"interface registry missing {command}")

    notes = NOTES.read_text(encoding="utf-8")
    if "from 0.4.0 to the intended 1.0.0 release" not in notes:
        raise SystemExit("release notes baseline mismatch")
    if "Status: unreleased" not in notes:
        raise SystemExit("release notes must remain unreleased")

    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    print(json.dumps({"commit": commit, "tree": tree, "version": "1.0.0"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
