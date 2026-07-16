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
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json"
EXPECTED_SCENARIO_ID = "CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED_TOP_LEVEL = {
    "scenario_id", "title", "status", "semantic_authority", "bounds",
    "initial_state", "evidence_schema", "transitions", "interleaving",
    "invariants", "outputs",
}


def canonical_bytes(value: Any) -> bytes:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"{text}\n".encode("utf-8")


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
    raw = validate_scenario(json.loads(source.read_text(encoding="utf-8")))

    def rebuild(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: rebuild(value[key]) for key in sorted(value)}
        if isinstance(value, list):
            return [rebuild(item) for item in value]
        return value

    return rebuild(raw)


def implementation_b(source: Path) -> dict[str, Any]:
    parsed = validate_scenario(json.JSONDecoder().decode(source.read_text(encoding="utf-8")))
    value = json.loads(json.dumps(parsed, ensure_ascii=False))
    output: dict[str, Any] = {}
    stack: list[tuple[Any, Any, Any]] = [(output, key, value[key]) for key in sorted(value, reverse=True)]
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
    pairs = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=lambda items: ("__object__", items))

    def materialize(value: Any) -> Any:
        if isinstance(value, tuple) and len(value) == 2 and value[0] == "__object__":
            return {str(key): materialize(item) for key, item in sorted(value[1], key=lambda pair: str(pair[0]))}
        if isinstance(value, list):
            return [materialize(item) for item in value]
        return value

    result = materialize(pairs)
    return validate_scenario(json.loads(canonical_bytes(result)))


def worker(kind: str, source: Path, destination: Path) -> int:
    implementations: dict[str, Callable[[Path], dict[str, Any]]] = {
        "a": implementation_a,
        "b": implementation_b,
        "c": implementation_c,
    }
    destination.write_bytes(canonical_bytes(implementations[kind](source)))
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

    cases: list[dict[str, Any]] = []
    reference = canonical[0]
    for name, candidate in mutations:
        try:
            rejected = canonical_bytes(validate_scenario(candidate)) != reference
        except Exception:
            rejected = True
        cases.append({"case": name, "rejected": rejected})

    malformed = [
        ("malformed-json", b"{not-json\n"),
        ("wrong-root", b"[]\n"),
        ("missing-id", canonical_bytes({"title": "adversarial"})),
    ]
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
        "claim_class": "bounded multi-implementation robustness",
        "external_replication": False,
    }


def run_worker(kind: str, work: Path) -> Path:
    private_input = work / "scenario.json"
    destination = work / "output.json"
    shutil.copyfile(SCENARIO, private_input)
    env = {"PYTHONHASHSEED": "0", "PATH": os.environ.get("PATH", "")}
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            kind,
            "--source",
            str(private_input),
            "--output",
            str(destination),
        ],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"compiler-{kind} failed:\n{result.stdout}{result.stderr}")
    return destination


def isolated_run(temp_root: Path, run_name: str) -> dict[str, Any]:
    run_root = temp_root / run_name
    run_root.mkdir()
    output_paths: list[Path] = []
    for kind in ("a", "b", "c"):
        work = run_root / f"compiler-{kind}"
        work.mkdir()
        output_paths.append(run_worker(kind, work))

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
