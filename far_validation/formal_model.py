from __future__ import annotations

import itertools
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .trust import HMACTrust, TrustError, read_attestation, write_attestation


@dataclass(frozen=True)
class AbstractRun:
    dependencies: tuple[tuple[int, ...], ...]
    outcomes: tuple[bool, ...]
    states: tuple[str, ...]
    execution_order: tuple[int, ...]

    @property
    def successful(self) -> bool:
        return all(state == "passed" for state in self.states)


def simulate(dependencies: tuple[tuple[int, ...], ...], outcomes: tuple[bool, ...]) -> AbstractRun:
    size = len(dependencies)
    states = ["pending"] * size
    order: list[int] = []
    while any(state == "pending" for state in states):
        ready = [
            index for index, state in enumerate(states)
            if state == "pending" and all(states[dep] != "pending" for dep in dependencies[index])
        ]
        if not ready:
            raise AssertionError("acyclic abstract graph became unschedulable")
        for index in ready:
            if any(states[dep] != "passed" for dep in dependencies[index]):
                states[index] = "blocked"
            else:
                states[index] = "passed" if outcomes[index] else "failed"
                order.append(index)
    return AbstractRun(dependencies, outcomes, tuple(states), tuple(order))


def dependency_graphs(size: int) -> Iterable[tuple[tuple[int, ...], ...]]:
    possible = [(left, right) for left in range(size) for right in range(left + 1, size)]
    for bits in itertools.product((False, True), repeat=len(possible)):
        deps: list[list[int]] = [[] for _ in range(size)]
        for enabled, (left, right) in zip(bits, possible):
            if enabled:
                deps[right].append(left)
        yield tuple(tuple(values) for values in deps)


def verify_run(run: AbstractRun) -> None:
    for index, deps in enumerate(run.dependencies):
        state = run.states[index]
        if state == "blocked":
            assert any(run.states[dep] != "passed" for dep in deps)
        if state in {"passed", "failed"}:
            assert all(run.states[dep] == "passed" for dep in deps)
        if any(run.states[dep] != "passed" for dep in deps):
            assert state == "blocked"
    for position, index in enumerate(run.execution_order):
        earlier = set(run.execution_order[:position])
        assert set(run.dependencies[index]) <= earlier
    assert run.successful == all(state == "passed" for state in run.states)


def verify_attestation_model() -> int:
    trust = HMACTrust(key=b"formal-model-key", trust_domain="formal", key_id="model")
    payload = {"cache_key": "abc", "check_id": "x", "result": {"status": "passed"}}
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "attestation.json"
        write_attestation(path, trust=trust, kind="cache-result", payload=payload)
        assert read_attestation(path, trust=trust, kind="cache-result") == payload
        original = json.loads(path.read_text(encoding="utf-8"))
        fields = [
            ("kind", "certificate"),
            ("trust_domain", "other"),
            ("key_id", "other"),
            ("payload", {"cache_key": "tampered"}),
            ("signature", "0" * 64),
        ]
        rejected = 0
        for field, value in fields:
            mutated = dict(original)
            mutated[field] = value
            path.write_text(json.dumps(mutated), encoding="utf-8")
            try:
                read_attestation(path, trust=trust, kind="cache-result")
            except TrustError:
                rejected += 1
            else:
                raise AssertionError(f"attestation mutation accepted: {field}")
        return rejected


def exhaustive_model_check(max_checks: int = 4) -> dict[str, int]:
    graphs = 0
    runs = 0
    for size in range(1, max_checks + 1):
        for dependencies in dependency_graphs(size):
            graphs += 1
            for outcomes in itertools.product((False, True), repeat=size):
                run = simulate(dependencies, outcomes)
                verify_run(run)
                runs += 1
    attestation_mutations = verify_attestation_model()
    return {"max_checks": max_checks, "graphs": graphs, "runs": runs, "attestation_mutations": attestation_mutations}


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Exhaustively model-check the validation engine state machine")
    parser.add_argument("--max-checks", type=int, default=4)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = exhaustive_model_check(args.max_checks)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "validation engine formal model: PASS "
            f"({result['graphs']} DAGs, {result['runs']} runs, "
            f"{result['attestation_mutations']} hostile attestations rejected)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
