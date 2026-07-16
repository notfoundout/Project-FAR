#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json"
EXPECTED_SCENARIO_ID = "CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED_TOP_LEVEL = {
    "scenario_id", "title", "status", "semantic_authority", "bounds",
    "initial_state", "evidence_schema", "transitions", "interleaving",
    "invariants", "outputs",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def validate_scenario(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("scenario must be an object")
    missing = REQUIRED_TOP_LEVEL - set(value)
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    if value["scenario_id"] != EXPECTED_SCENARIO_ID:
        raise ValueError("unexpected scenario_id")
    transitions = value["transitions"]
    if not isinstance(transitions, list) or not transitions:
        raise ValueError("transitions must be a non-empty list")
    ids = [item.get("id") for item in transitions if isinstance(item, dict)]
    if len(ids) != len(transitions) or len(set(ids)) != len(ids):
        raise ValueError("transition ids must be present and unique")
    return value


def implementation_a(source: Path) -> dict[str, Any]:
    # Direct recursive reconstruction; no shared generated artifacts.
    raw = validate_scenario(json.loads(source.read_text(encoding="utf-8")))

    def rebuild(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: rebuild(value[key]) for key in sorted(value)}
        if isinstance(value, list):
            return [rebuild(item) for item in value]
        return value

    return rebuild(raw)


def implementation_b(source: Path) -> dict[str, Any]:
    # Token round-trip followed by an independently written iterative normalizer.
    parsed = validate_scenario(json.JSONDecoder().decode(source.read_text(encoding="utf-8")))
    encoded = json.dumps(parsed, ensure_ascii=False)
    value = json.loads(encoded)
    stack: list[tuple[Any, Any, Any]] = []
    output: dict[str, Any] = {}
    for key in sorted(value):
        stack.append((output, key, value[key]))
    while stack:
        parent, key, current = stack.pop()
        if isinstance(current, dict):
            child: dict[str, Any] = {}
            parent[key] = child
            for nested in sorted(current, reverse=True):
                stack.append((child, nested, current[nested]))
        elif isinstance(current, list):
            child_list: list[Any] = [None] * len(current)
            parent[key] = child_list
            for index in range(len(current) - 1, -1, -1):
                stack.append((child_list, index, current[index]))
        else:
            parent[key] = current
    return validate_scenario(output)


def implementation_c(source: Path) -> dict[str, Any]:
    # Independent path: parse ordered pairs, recursively normalize, then reparse.
    text = source.read_text(encoding="utf-8")
    pairs = json.loads(text, object_pairs_hook=list)

    def materialize(value: Any) -> Any:
        if isinstance(value, list):
            if all(isinstance(item, tuple) and len(item) == 2 for item in value):
                return {str(k): materialize(v) for k, v in sorted(value, key=lambda item: str(item[0]))}
            return [materialize(item) for item in value]
        return value

    result = materialize(pairs)
    return validate_scenario(json.loads(canonical_bytes(result)))


def worker(kind: str, source: Path, destination: Path) -> int:
    implementations = {"a": implementation_a, "b": implementation_b, "c": implementation_c}
    result = implementations[kind](source)
    destination.write_bytes(canonical_bytes(result))
    return 0


def verifier(paths: list[Path]) -> dict[str, Any]:
    raw = [path.read_bytes() for path in paths]
    parsed = [validate_scenario(json.loads(blob)) for blob in raw]
    canonical = [canonical_bytes(item) for item in parsed]
    equal = all(blob == canonical[0] for blob in canonical[1:])
    byte_equal = all(blob == raw[0] for blob in raw[1:])
    if not equal or not byte_equal:
        raise ValueError("implementation outputs differ")

    mutations: list[tuple[str, Any]] = []
    removed = json.loads(raw[0])
    removed["transitions"] = removed["transitions"][:-1]
    mutations.append(("remove-transition", removed))
    changed = json.loads(raw[0])
    changed["interleaving"]["simultaneous_execution"] = True
    mutations.append(("change-interleaving", changed))
    duplicate = json.loads(raw[0])
    duplicate["transitions"].append(dict(duplicate["transitions"][0]))
    mutations.append(("duplicate-transition-id", duplicate))
    malformed: list[tuple[str, bytes]] = [
        ("malformed-json", b"{not-json\n"),
        ("wrong-root", b"[]\n"),
        ("missing-id", canonical_bytes({"title": "adversarial"})),
    ]

    cases: list[dict[str, Any]] = []
    reference = canonical[0]
    for name, candidate in mutations:
        try:
            candidate_bytes = canonical_bytes(validate_scenario(candidate))
            rejected = candidate_bytes != reference
        except Exception:
            rejected = True
        cases.append({"case": name, "rejected": rejected})
    for name, blob in malformed:
        try:
            validate_scenario(json.loads(blob))
            rejected = False
        except Exception:
            rejected = True
        cases.append({"case": name, "rejected": rejected})
    if not all(case["rejected"] for case in cases):
        raise ValueError("mutation or adversarial case escaped detection")
    return {
        "status": "pass",
        "digest": hashlib.sha256(reference).hexdigest(),
        "implementations": len(paths),
        "byte_identical": byte_equal,
        "mutation_and_adversarial_cases": cases,
        "claim_class": "internal implementation replication",
        "external_replication": False,
    }


def isolated_run(temp_root: Path, run_name: str) -> dict[str, Any]:
    run_root = temp_root / run_name
    run_root.mkdir()
    output_paths: list[Path] = []
    for kind in ("a", "b", "c"):
        work = run_root / f"compiler-{kind}"
        work.mkdir()
        private_input = work / "scenario.json"
        shutil.copyfile(SCENARIO, private_input)
        destination = work / "output.json"
        env = {"PYTHONHASHSEED": "0", "PATH": os.environ.get("PATH", "")}
        subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--worker", kind, "--source", str(private_input), "--output", str(destination)],
            cwd=work,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        output_paths.append(destination)
    verifier_work = run_root / "verifier"
    verifier_work.mkdir()
    frozen: list[Path] = []
    for index, source in enumerate(output_paths):
        target = verifier_work / f"candidate-{index}.json"
        shutil.copyfile(source, target)
        frozen.append(target)
    return verifier(frozen)


def check() -> int:
    with tempfile.TemporaryDirectory(prefix="cre002-robustness-") as directory:
        root = Path(directory)
        first = isolated_run(root, "run-1")
        second = isolated_run(root, "run-2")
    deterministic = first["digest"] == second["digest"] and first == second
    report = dict(first)
    report["deterministic_rerun"] = deterministic
    report["status"] = "pass" if deterministic else "fail"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--worker", choices=["a", "b", "c"])
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        if args.source is None or args.output is None:
            parser.error("--worker requires --source and --output")
        return worker(args.worker, args.source, args.output)
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
