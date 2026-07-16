#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from dataclasses import dataclass
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class State:
    flags: tuple[tuple[str, bool], ...]
    evidence: tuple[tuple[str, str, str], ...]
    history: tuple[str, ...]
    active_rules: tuple[str, ...]
    modification_count: int
    choices: tuple[str, ...]
    priority_defeat: bool
    terminal_reason: str | None

    def data(self) -> dict[str, Any]:
        return {
            "booleans": dict(self.flags),
            "evidence_log": [list(x) for x in self.evidence],
            "action_history": list(self.history),
            "active_rules": list(self.active_rules),
            "modification_count": self.modification_count,
            "nondeterministic_outcomes": list(self.choices),
            "priority_defeat_occurred": self.priority_defeat,
            "terminal_reason": self.terminal_reason,
        }


def initial(model: dict[str, Any]) -> State:
    source = model["initial_state"]
    return State(
        tuple(sorted(source["booleans"].items())),
        tuple(tuple(x) for x in source.get("evidence_log", [])),
        tuple(source.get("action_history", [])),
        tuple(sorted(source["active_rules"])),
        int(source.get("modification_count", 0)),
        (), False, None,
    )


def changed(s: State, *, flags: dict[str, bool] | None = None,
            evidence: tuple[tuple[str, str, str], ...] | None = None,
            action: str | None = None, active: tuple[str, ...] | None = None,
            modifications: int | None = None, choice: str | None = None,
            priority_defeat: bool | None = None,
            reason: str | None = None) -> State:
    values = dict(s.flags)
    values.update(flags or {})
    return State(
        tuple(sorted(values.items())),
        s.evidence if evidence is None else evidence,
        s.history + ((action,) if action else ()),
        s.active_rules if active is None else tuple(sorted(active)),
        s.modification_count if modifications is None else modifications,
        s.choices + ((choice,) if choice else ()),
        s.priority_defeat if priority_defeat is None else priority_defeat,
        s.terminal_reason if reason is None else reason,
    )


def has_evidence(s: State, claim: str, source: str, reliability: str) -> bool:
    return (claim, source, reliability) in s.evidence


def successors(model: dict[str, Any], s: State, include_halt: bool = True) -> list[tuple[str, State]]:
    b, active, fired = dict(s.flags), set(s.active_rules), set(s.history)
    if b["system_halted"]:
        return []
    out: list[tuple[str, State]] = []
    if "T_record_a" not in fired:
        for value in (True, False):
            claim = f"sensor_a_positive={str(value).lower()}"
            ev = s.evidence + ((claim, "sensor_a", "high"),)
            out.append((f"T_record_a:{value}", changed(s, flags={"sensor_a_positive": value}, evidence=ev, action="T_record_a", choice=f"record_a={str(value).lower()}")))
    if "T_record_b" not in fired:
        for value, reliability in ((True, "high"), (False, "low")):
            claim = f"sensor_b_positive={str(value).lower()}"
            ev = s.evidence + ((claim, "sensor_b", reliability),)
            out.append((f"T_record_b:{value}", changed(s, flags={"sensor_b_positive": value}, evidence=ev, action="T_record_b", choice=f"record_b={str(value).lower()}")))
    if not b["alarm_confirmed"] and "R_confirm" in active and b["sensor_a_positive"] and has_evidence(s, "sensor_a_positive=true", "sensor_a", "high") and (b["sensor_b_positive"] or b["manual_override"]):
        out.append(("T_confirm", changed(s, flags={"alarm_confirmed": True}, action="T_confirm")))
    if not b["manual_override"] and "R_override" in active and has_evidence(s, "manual_override=true", "operator", "high"):
        out.append(("T_override", changed(s, flags={"manual_override": True}, action="T_override", priority_defeat=True)))
    for suffix in ("alpha", "beta"):
        rule = f"R_dispatch_{suffix}"
        if rule in active and b["alarm_confirmed"] and b[f"route_{suffix}_open"] and not b[f"{suffix}_dispatched"]:
            out.append((f"T_dispatch_{suffix}", changed(s, flags={f"{suffix}_dispatched": True}, action=f"T_dispatch_{suffix}")))
    if "R_modify" in active and b["alarm_confirmed"] and s.modification_count == 0 and (b["alpha_dispatched"] ^ b["beta_dispatched"]):
        target = "R_dispatch_beta" if b["alpha_dispatched"] else "R_dispatch_alpha"
        out.append(("T_modify", changed(s, active=tuple(x for x in active if x != target), modifications=1, action="T_modify")))
    if "R_contain" in active and not b["incident_contained"] and b["alarm_confirmed"] and (b["alpha_dispatched"] or b["beta_dispatched"]):
        out.append(("T_contain", changed(s, flags={"incident_contained": True}, action="T_contain")))
    if include_halt and "R_halt" in active:
        nonhalt = successors(model, s, False)
        blocked = all(
            f"R_dispatch_{x}" not in active or not (b["alarm_confirmed"] and b[f"route_{x}_open"] and not b[f"{x}_dispatched"])
            for x in ("alpha", "beta")
        )
        deadlock = not nonhalt and blocked
        if b["incident_contained"] or deadlock:
            reason = "contained" if b["incident_contained"] else "deadlock"
            out.append(("T_halt", changed(s, flags={"system_halted": True}, action="T_halt", reason=reason)))
    return out


def semantic_contract(model: dict[str, Any]) -> dict[str, Any]:
    transitions = {item["id"]: item for item in model["transitions"]}
    return {
        "nondeterministic_alternatives": {
            key: transitions[key].get("nondeterministic_alternatives", [])
            for key in ("T_record_a", "T_record_b")
        },
        "interleaving": model["interleaving"],
        "priorities": model["initial_state"]["priorities"],
        "provenance_guards": {
            key: transitions[key].get("guard_expression")
            for key in ("T_confirm", "T_override")
        },
        "rule_modification": transitions["T_modify"],
        "invariants": model["invariants"],
        "outputs": model["outputs"],
    }


def explore(model: dict[str, Any]) -> dict[str, Any]:
    start = initial(model)
    queue, seen, edges = deque([start]), {start}, []
    while queue:
        state = queue.popleft()
        for label, nxt in successors(model, state):
            edges.append((canonical(state.data()), label, canonical(nxt.data())))
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    terminals = [s for s in seen if dict(s.flags)["system_halted"]]
    states = sorted(canonical(s.data()) for s in seen)
    return {
        "state_count": len(seen),
        "edge_count": len(edges),
        "states_digest": hashlib.sha256(canonical(states).encode()).hexdigest(),
        "edges_digest": hashlib.sha256(canonical(sorted(edges)).encode()).hexdigest(),
        "semantic_contract_digest": hashlib.sha256(canonical(semantic_contract(model)).encode()).hexdigest(),
        "terminal_count": len(terminals),
        "terminal_reasons": dict(sorted(Counter(s.terminal_reason for s in terminals).items())),
        "required_outputs_preserved": all({"booleans", "evidence_log", "action_history", "active_rules", "nondeterministic_outcomes", "priority_defeat_occurred", "terminal_reason"}.issubset(s.data()) for s in terminals),
    }
